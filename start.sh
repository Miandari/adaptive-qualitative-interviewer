#!/bin/bash

# ESM Chatbot Quick Start Script

echo "====================================="
echo "ESM Chatbot Quick Start"
echo "====================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your API keys before continuing!"
    echo ""
    echo "Edit the file with:"
    echo "  nano .env"
    echo ""
    read -p "Press Enter when you've configured your API keys..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create exports directory
mkdir -p exports
echo "✅ Exports directory created"

echo ""
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "Choose how to run the chatbot:"
echo ""
echo "1. Streamlit Web Interface (Recommended):"
echo "   streamlit run interfaces/streamlit_app.py"
echo ""
echo "2. FastAPI REST API:"
echo "   uvicorn interfaces.fastapi_app:app --reload"
echo ""
echo "3. Python Library Example:"
echo "   python examples/standalone.py"
echo ""

# Ask user which interface to start
read -p "Which interface would you like to start? (1/2/3/skip): " choice

case $choice in
    1)
        echo ""
        echo "Starting Streamlit interface..."
        echo "Open http://localhost:8501 in your browser"
        streamlit run interfaces/streamlit_app.py
        ;;
    2)
        echo ""
        echo "Starting FastAPI server..."
        echo "API docs at http://localhost:8000/docs"
        uvicorn interfaces.fastapi_app:app --reload
        ;;
    3)
        echo ""
        echo "Running standalone example..."
        python examples/standalone.py
        ;;
    *)
        echo ""
        echo "You can start the chatbot later with one of the commands above."
        ;;
esac
