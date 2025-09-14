# app.py
from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/rf_pipeline.joblib")

class EmailRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: EmailRequest):
    pred = model.predict([request.text])[0]
    proba = model.predict_proba([request.text])[0].max()
    label_map = {0: "ham", 1: "spam"}
    time.sleep(1)  # Simulate processing delay
    return {"label": label_map[int(pred)], "confidence": float(proba)}

@app.get("/")
def read_root():
        return {"message": "Hello, World!"}
