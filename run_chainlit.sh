#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set Python path to current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run chainlit
chainlit run interfaces/chainlit_app.py
