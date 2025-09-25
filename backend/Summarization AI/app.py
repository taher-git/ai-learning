from fastapi import FastAPI, UploadFile, File, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import whisper
import tempfile
import os

app = FastAPI()
client = OpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load Whisper model once at startup
whisper_model = whisper.load_model("tiny")  # can be "tiny", "base", "small", "medium", "large"

@app.post("/summarize/")
async def summarize_meeting(
    file: UploadFile = File(...),
    mode: str = Query("local", description="Choose 'local' or 'api' for transcription"),
    summary_type: str = Form("paragraph")   # default = paragraph
):
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

    # Step 2: Summarize transcript with GPT
    style_prompt = "Summarize in a short paragraph." if summary_type == "paragraph" \
                   else "Summarize in concise bullet points."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a meeting summarizer."},
            {"role": "user", "content": f"{style_prompt}\nTranscript:\n{transcript}"}
        ]
    )
    summary = resp.choices[0].message.content

    # Step 3: Extract Action Items
    action_items = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a meeting assistant."},
            {"role": "user", "content": f"From this transcript, extract clear actionable next steps:\n{transcript}"}
        ]
    ).choices[0].message.content
    # Clean up temp file
    os.remove(tmp_path)

    return {
        "mode": mode,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items
    }
