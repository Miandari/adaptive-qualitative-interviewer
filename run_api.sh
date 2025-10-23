#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set Python path to current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run FastAPI server
uvicorn interfaces.fastapi_app:app --reload
