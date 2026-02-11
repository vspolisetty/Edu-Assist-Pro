@echo off
echo 🤖 Edu Assist RAG Chatbot Setup
echo ==========================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Please run this script from the backend directory
    echo    Current directory should contain app.py
    pause
    exit /b 1
)

echo ✅ Found app.py in current directory

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo ✅ Virtual environment ready

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    echo    Check your internet connection and try again
    pause
    exit /b 1
)

echo ✅ Packages installed successfully

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️ No .env file found. Creating from template...
    copy .env.example .env
    echo.
    echo 📝 IMPORTANT: Please edit .env file and add your GROQ_API_KEY
    echo    1. Get a free API key from: https://console.groq.com/keys
    echo    2. Edit .env file
    echo    3. Replace 'your_groq_api_key_here' with your actual key
    echo.
    pause
)

REM Test setup
echo 🔍 Testing setup...
python test_setup.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Setup test failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Starting Edu Assist backend server...
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo    Frontend: Open your static/index.html in browser
echo.
echo � Tip: Look for the 🧠 icon in your website logo to confirm RAG is connected
echo.

REM Start the server
python app.py

pause
