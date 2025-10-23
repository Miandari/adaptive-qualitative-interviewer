#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set Python path to current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run streamlit
streamlit run interfaces/streamlit_app.py
