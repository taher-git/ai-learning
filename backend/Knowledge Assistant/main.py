from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.file_utils import read_pdf_by_path
from utils.splitter import split_text
from utils.embeddings import get_embeddings, model
from utils.vector_store import store_embeddings, search_similar_chunks, file_exists, read_file, build_prompt, list_docs,delete_doc, save_doc_embeddings
from openai import OpenAI
from typing import List, Dict


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

@app.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...)):
    # Step 1: Save file locally
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 2: Extract text
    text = read_pdf_by_path(file_path)

    # Step 3: Split text into chunks
    chunks = split_text(text, chunk_size=500)

    # Step 4: Get embeddings
    embeddings = get_embeddings(chunks)

    # Step 5: Store in FAISS
    store_embeddings(embeddings, chunks)

    return {"status": "success", "chunks_stored": len(chunks)}

@app.post("/upload-docs")
async def upload_docs(files: List[UploadFile] = File(...)):
    all_docs = []
    for file in files:
        text = await read_file(file)
        chunks = split_text(text, chunk_size=500)
        save_doc_embeddings(file.filename, chunks, model)
        all_docs.append(file.filename)

    return {"status": "success", "uploaded": all_docs}

client = OpenAI()

@app.post("/ask")
async def ask_question(question: str = Form( "true")):
    if not file_exists():
        return {"error": "No documents indexed yet. Please upload first."}
    
    # Step 1: Retrieve top chunks from FAISS
    top_chunks = search_similar_chunks(question, model, top_k=3)
    context = "\n\n".join(top_chunks)

    # Step 2: Build the prompt for LLM
    prompt = f"""
    You are a document assistant. Use only the information below to answer:

    Context:
    {context}

    Question:
    {question}

    Answer concisely:
    """

    # Step 3: Get AI-generated answer
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer,
        "context_used": top_chunks
    }

@app.post("/ask-multiple")
async def ask_question_multiple(question: str = Form( "true")):
    global chat_sessions
    session_id = "111"
    history = chat_sessions.get(session_id, [])
    prompt = build_prompt(question, model, history)
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
                {"role": "user", "content": prompt}
            ]
        )

    answer = response.choices[0].message.content
    # Save to session memory
    history.append({"user": question, "ai": answer})
    chat_sessions[session_id] = history
    return {
        "question": question,
        "answer": answer,
        "history": history
    }

@app.get("/list-docs")
def get_all_docs():
    return list_docs()

@app.delete("/delete-doc/{doc_name}")
def delete_selected_doc(doc_name: str):
    try:
        delete_doc(doc_name)
        return {"status": "success", "message": f"Document {doc_name} deleted."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# knowledge_index.faiss