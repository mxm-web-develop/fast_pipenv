#!/bin/sh
# start_fastapi.sh
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8999 --reload
