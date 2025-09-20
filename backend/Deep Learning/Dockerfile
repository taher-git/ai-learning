# Dockerfile
FROM python:3.10-slim

# 1) system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    git \
    wget \
  && rm -rf /var/lib/apt/lists/*

# 2) create app directory and a non-root user
WORKDIR /app
RUN useradd --create-home appuser
USER appuser

# 3) copy only requirements first (for better caching)
COPY --chown=appuser:appuser requirements.txt /app/requirements.txt

# 4) install Python deps
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5) copy app code
COPY --chown=appuser:appuser . /app

# 6) expose port and set env vars (optional defaults)
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/models/transformers_cache

# 7) entrypoint and default command
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["/app/entrypoint.sh"]
