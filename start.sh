#!/bin/sh
set -e

echo "Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit..."
exec streamlit run Frontend/streamlit_app.py \
  --server.port ${PORT:-8501} \
  --server.address 0.0.0.0