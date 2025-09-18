from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pipeline once at startup
# classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
classifier = pipeline("text-classification", model="./results/checkpoint-500")

class Message(BaseModel):
    text: str

LABELS = {"LABEL_0": "ham", "LABEL_1": "spam"}

@app.post("/predict")
async def predict(message: Message):
    result = classifier(message.text)[0]
    time.sleep(1)  # Simulate processing delay
    return {
        "label": LABELS.get(result["label"], result["label"]),
        "confidence": result["score"]
    }

