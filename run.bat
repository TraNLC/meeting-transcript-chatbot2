@echo off
echo ========================================
echo Meeting Transcript Chatbot
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your OPENAI_API_KEY
    echo.
    pause
    exit /b 1
)

REM Install requirements if needed
echo Checking dependencies...
pip install -q -r requirements.txt
echo.

REM Run Gradio app
echo Starting application...
echo Application will open at: http://localhost:7860
echo.
python src/ui/gradio_app.py

pause
