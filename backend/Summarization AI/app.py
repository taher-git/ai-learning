from fastapi import FastAPI, UploadFile, File, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, RetrievalQA,ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
import whisper
import tempfile
import os

app = FastAPI()
client = OpenAI()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
vectorstore = None
qa_chain = None  # will hold retriever + memory chain
transcript = ""
mode = "local"  # default mode: local or api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load Whisper model once at startup
whisper_model = whisper.load_model("tiny")  # can be "tiny", "base", "small", "medium", "large"

# Prompt for summarization
prompt = ChatPromptTemplate.from_template("""
You are a meeting summarizer.
Summarize the following transcript into {style}:

Transcript:
{transcript}
""")
summarize_chain = LLMChain(llm=llm, prompt=prompt)

@app.post("/upload/")
async def uploadMeeting(
    file: UploadFile = File(...),
):
    global transcript, qa_chain, vectorstore,mode
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Step 1: Transcribe
    if mode == "local":
        result = whisper_model.transcribe(tmp_path)
        transcript = result["text"]

    elif mode == "api":
        with open(tmp_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",  # OpenAI Whisper API
                file=audio_file
            )
        transcript = response.text
    else:
        return {"error": "Invalid mode. Use 'local' or 'api'."}
    # Split transcript into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([transcript])

    # Build embeddings + FAISS vectorstore
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Create memory-enabled chain
    memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
    )
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    ) 
    # Clean up temp file
    os.remove(tmp_path)

    return {
        "mode": mode,
        "transcript": transcript,
    }


@app.post("/summarize/")
async def summarizeMeeting(
    summary_type: str = Form("paragraph")   # default = paragraph
):
    # Step 2: Summarize transcript with GPT
    # style_prompt = "Summarize in a short paragraph." if summary_type == "paragraph" \
    #                else "Summarize in concise bullet points."
    # resp = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a meeting summarizer."},
    #         {"role": "user", "content": f"{style_prompt}\nTranscript:\n{transcript}"}
    #     ]
    # )
    # summary = resp.choices[0].message.content

    # Summarization via LangChain
    style = "a short paragraph" if summary_type == "paragraph" else "concise bullet points"
    summary = summarize_chain.run(transcript=transcript, style=style)

    return {
        "summary": summary,
    }


@app.get("/actions/")
async def nextActions():
    # Step 3: Extract Action Items
    action_items = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a meeting assistant."},
            {"role": "user", "content": f"From this transcript, extract clear actionable next steps:\n{transcript}"}
        ]
    ).choices[0].message.content

    return {
        "action_items": action_items
    }

@app.post("/ask/")
async def askQuestion(question: str = Form(...)):
    """
    Ask a question about the uploaded transcript.
    """
    if vectorstore is None:
        return {"error": "No transcript uploaded yet."}
    global qa_chain
    # retriever = vectorstore.as_retriever()
    # qa_chain = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     retriever=retriever,
    #     chain_type="stuff"
    # )
    # answer = qa_chain.run(question)

    result = qa_chain.invoke({"question": question})
    answer = result['answer']
    return {
        "question": question, 
        "answer": answer,
        "history": [(m.content if hasattr(m, "content") else str(m)) for m in result["chat_history"]]
}
