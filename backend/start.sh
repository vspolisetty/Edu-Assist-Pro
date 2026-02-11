#!/bin/bash

# Edu Assist RAG Chatbot Setup and Run Script

echo "🤖 Edu Assist RAG Chatbot Setup"
echo "=========================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "app.py" ]]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Install requirements
echo "📥 Installing Python packages..."
pip install -r requirements.txt

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your GROQ_API_KEY"
    echo "   You can get a free API key from: https://console.groq.com/keys"
    read -p "Press Enter to continue after setting up your API key..."
fi

# Check if GROQ_API_KEY is set
source .env
if [[ -z "$GROQ_API_KEY" || "$GROQ_API_KEY" == "your_groq_api_key_here" ]]; then
    echo "❌ GROQ_API_KEY is not set in .env file"
    echo "   Please edit .env file and add your API key from https://console.groq.com/keys"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Edu Assist backend server..."
echo "   Backend API: http://localhost:8000"
echo "   Frontend: Open index.html in your browser"
echo ""
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
echo ""

# Start the server
python app.py
