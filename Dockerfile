# Dockerfile — package the RAG service into a portable image.
# Build:  docker build -t triage-assistant .
# Run:    docker run -p 8000:8000 -e ANTHROPIC_API_KEY=... triage-assistant

# 1. Base image: official, slim Python. "slim" = small (no build extras) but still Debian.
FROM python:3.12-slim

# 2. System library torch/faiss need for CPU math (OpenMP). Clean the apt cache to stay small.
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Everything runs under /app inside the container.
WORKDIR /app

# 4. Cache the embedding model INSIDE the image (see step 6) and unbuffer logs so they
#    stream to CloudWatch in real time instead of sticking in a buffer.
ENV HF_HOME=/app/.cache \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache \
    PYTHONUNBUFFERED=1

# 5. Install dependencies FIRST, in their own layer. Docker caches layers; as long as
#    requirements.txt is unchanged, this expensive step is reused on every rebuild.
#    Install the CPU-ONLY PyTorch wheel explicitly (from PyTorch's CPU index) BEFORE the
#    rest, so sentence-transformers doesn't drag in the multi-GB CUDA/GPU stack. Fargate
#    has no GPU, so CUDA libs would be pure bloat (image ~6-8GB -> ~1-1.5GB with CPU torch).
COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# 6. Pre-download the embedding model at BUILD time so it's baked into the image.
#    Result: fast cold starts and no network dependency when the container boots.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# 7. Copy the application code + knowledge base (changes often -> kept AFTER deps so the
#    dependency layer above stays cached when you only edit code).
COPY rag.py app.py triage.py ./
COPY kb ./kb

# 8. Security: run as a non-root user, not root. Own the app dir so the model cache is readable.
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# 9. Document that the service listens on 8000 (this is metadata; -p does the real mapping).
EXPOSE 8000

# 10. Start the ASGI server. --host 0.0.0.0 is REQUIRED in a container so it accepts
#     connections from outside; 127.0.0.1 would only be reachable inside the container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
