# app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import time
import logging
from fastapi.middleware.cors import CORSMiddleware

MODEL_NAME = os.environ.get("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
# TRANSFORMERS_CACHE can be set to a mounted directory so models persist outside the container.


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = None

class Message(BaseModel):
    text: str
LABELS = {"POSITIVE": "ham", "NEGATIVE": "spam"}

@app.on_event("startup")
def load_model():
    global classifier
    classifier = pipeline("text-classification", model=MODEL_NAME)

@app.post("/predict")
def predict(msg: Message):
    try:
        res = classifier(msg.text)[0]
        time.sleep(1)  # Simulate processing delay 
        # raise Exception("Simulated error")  # Simulate an error for testing
        # Optional: map LABEL_0/LABEL_1 to ham/spam if model uses that mapping
        return {"label": LABELS.get(res["label"], res["label"]), "confidence": float(res["score"])}
    
    
    except Exception as e:
        logging.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
