# � Edu Assist Pro: Corporate Training Platform

An AI-powered corporate training platform with RAG (Retrieval Augmented Generation) capabilities. Built for enterprise teams, featuring PDF knowledge base integration, web search fallback, and a professional training interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🤖 **AI-Powered Training Assistant** - Intelligent responses using Groq LLM (Llama models)
- 📚 **RAG System** - Search uploaded training documents for context-aware answers
- 🔍 **Web Search Fallback** - Automatically searches the web when documents don't have answers
- 📋 **Training Modules** - Compliance, Security, Leadership, Technical Skills & more
- 📊 **Training Analytics** - Track courses completed, certifications, and training hours
- 🌓 **Dark/Light Theme** - Professional look for corporate environments
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 🖼️ Screenshots

| Login Portal | Training Chat | Training Dashboard |
|------------|----------------|-----------|
| Professional corporate login | AI training assistant | Progress & analytics |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Groq API Key** (Free) - [Get API Key](https://console.groq.com/keys)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/vspolisetty/Edu-AI.git
cd Edu-AI
```

#### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note:** If you encounter version conflicts, upgrade these packages:
```bash
pip install --upgrade sentence-transformers groq
```

#### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
# Replace 'your_groq_api_key_here' with your actual key
```

**`.env` file contents:**
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

#### 4. Start the Server

```bash
# From the project root directory
cd ..
python3 simple_launch.py
```

Or manually:
```bash
cd backend
python3 app.py
```

#### 5. Access the Application

Open your browser and go to:
- **Login Page**: http://localhost:3000/static/login.html
- **Demo Credentials**: Username: `test`, Password: `test`

---

## 📦 Dependencies

### Backend (Python)

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.104.1 | Web framework |
| `uvicorn` | 0.24.0 | ASGI server |
| `groq` | Latest | Groq LLM API client |
| `sentence-transformers` | Latest | Text embeddings |
| `PyMuPDF` | 1.23.14 | PDF processing |
| `numpy` | 1.24.4 | Numerical operations |
| `aiohttp` | 3.9.1 | Async HTTP client |
| `python-dotenv` | 1.0.0 | Environment variables |
| `beautifulsoup4` | 4.12.2 | HTML parsing |
| `requests` | 2.31.0 | HTTP requests |

### Frontend

- Pure HTML5, CSS3, JavaScript (ES6+)
- Material Icons (Google Fonts)
- No build step required!

---

## 📁 Project Structure

```
Edu-AI/
├── backend/
│   ├── app.py                    # FastAPI main application
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment template
│   ├── .env                      # Your API keys (create this)
│   ├── vector_store.db           # SQLite vector database
│   ├── documents/                # PDF knowledge base
│   │   ├── Math/
│   │   │   └── Math Textbook.pdf
│   │   └── Science/
│   │       └── Science Text.pdf
│   └── services/
│       ├── groq_service.py       # Groq LLM integration
│       ├── rag_engine.py         # RAG orchestration
│       ├── vector_store.py       # Vector database
│       ├── pdf_processor.py      # PDF text extraction
│       └── web_search.py         # Web search fallback
├── static/
│   ├── index.html                # Chat interface
│   ├── dashboard.html            # User dashboard
│   ├── login.html                # Login page
│   ├── script.js                 # Main JavaScript
│   ├── dashboard.js              # Dashboard logic
│   ├── rag-integration.js        # RAG features
│   ├── style.css                 # Main styles
│   └── images/                   # Assets
├── simple_launch.py              # Easy launcher script
├── README.md                     # This file
└── .gitignore
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional - For enhanced web search
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
BING_SEARCH_API_KEY=your_bing_api_key

# Database
DATABASE_PATH=vector_store.db

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Server
API_HOST=0.0.0.0
API_PORT=3000
```

### Getting a Groq API Key (Free!)

1. Go to [console.groq.com](https://console.groq.com/keys)
2. Sign up for a free account (no credit card required)
3. Create a new API key
4. Copy and paste it into your `.env` file

---

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to login |
| `/health` | GET | Health check |
| `/api/chat` | POST | Send message, get AI response |
| `/api/upload-document` | POST | Upload PDF to knowledge base |
| `/api/documents` | GET | List all documents |
| `/api/documents/{id}` | DELETE | Remove a document |
| `/api/chat-history/{session_id}` | GET | Get conversation history |
| `/api/test` | GET | Test RAG system |
| `/docs` | GET | Swagger API documentation |

### Chat API Example

```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the quadratic formula?",
    "subject": "Mathematics",
    "eli5_mode": false
  }'
```

---

## 🎮 Usage Guide

### 1. Login
- Use demo credentials: `test` / `test`
- Or any username/password (demo mode accepts all)

### 2. Chat with AI
- Ask questions about any subject
- Toggle **ELI5 Mode** for simpler explanations
- Use the microphone for voice input (demo)

### 3. Upload PDFs
- Click the attach button (📎)
- Select a PDF file
- The AI will use it to answer questions

### 4. Track Progress
- View your dashboard for study stats
- Bookmark important Q&As
- Track XP and achievements

---

## 🛠️ Development

### Running in Development Mode

```bash
# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black backend/

# Lint code
flake8 backend/
```

### Adding New PDFs to Knowledge Base

1. Place PDF files in `backend/documents/<Subject>/`
2. Run the bulk processor:
```bash
cd backend
python3 bulk_process_pdfs.py
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### Groq API errors
- Verify your API key in `.env`
- Check your API quota at [console.groq.com](https://console.groq.com)

### Port already in use
```bash
# Find and kill the process
lsof -i :3000
kill -9 <PID>
```

### sentence-transformers import error
```bash
pip install --upgrade sentence-transformers huggingface-hub
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) - Fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Sentence Transformers](https://www.sbert.net/) - Text embeddings
- [Material Design](https://material.io/) - UI components

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/vspolisetty/Edu-AI/issues)
- **Email**: Contact the repository owner

---

**Made with ❤️ for students everywhere**