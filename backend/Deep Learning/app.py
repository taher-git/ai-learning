# app.py
import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from transformers import pipeline
import time
import logging
from fastapi.middleware.cors import CORSMiddleware
from auth import authenticate_user, create_access_token, decode_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
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

@app.middleware("http")
async def lifespan_middleware(request, call_next):
    global classifier
    if classifier is None:
        classifier = pipeline("text-classification", model=MODEL_NAME)
    response = await call_next(request)
    return response

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/auth/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": request.username},
        expires_delta=access_token_expires
    )
    return {"token": token}

@app.get("/protected")
def protected_route(token: str):
    user = decode_token(token)
    return {"msg": f"Hello {user['username']}, you are authenticated!"}

@app.post("/predict")
# @app.post("/predict", dependencies=[Depends(decode_token)])  # Uncomment to protect this endpoint
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
