#!/bin/bash

echo "========================================"
echo "Meeting Transcript Chatbot"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your OPENAI_API_KEY"
    echo ""
    exit 1
fi

# Install requirements if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt
echo ""

# Run Gradio app
echo "Starting application..."
echo "Application will open at: http://localhost:7860"
echo ""
python src/ui/gradio_app.py
