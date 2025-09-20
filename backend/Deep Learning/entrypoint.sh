#!/bin/bash
set -e

# Preload model into TRANSFORMERS_CACHE (optional)
python - <<'PY'
from transformers import pipeline
import os
model = os.environ.get("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
_ = pipeline("text-classification", model=model)
print("Model preloaded.")
PY

# Start FastAPI via Uvicorn
exec uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
