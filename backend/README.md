# Edu Assist RAG Chatbot Integration

This project integrates a Groq API-powered RAG (Retrieval Augmented Generation) chatbot into your existing Edu Assist website. The system can process PDFs, break them into chunks, and answer questions using both document knowledge and web search capabilities.

## 🌟 Features

- **RAG Architecture**: Retrieval Augmented Generation using Groq LLM
- **PDF Processing**: Upload and process PDF documents automatically
- **Vector Search**: Semantic similarity search using sentence transformers
- **Web Search Fallback**: Falls back to web search when no relevant documents found
- **ELI5 Mode**: Explain Like I'm 5 mode for simple explanations
- **Session Management**: Maintains conversation context
- **Source Attribution**: Shows sources for generated responses

## 🏗️ Architecture

```
Frontend (static/) ←→ FastAPI Backend ←→ Services:
                                        ├── Groq API (LLM)
                                        ├── Vector Store (SQLite + SentenceTransformers)
                                        ├── PDF Processor (PyMuPDF)
                                        └── Web Search (DuckDuckGo/Google/Bing)
```

## 📋 Prerequisites

- Python 3.8+
- Groq API Key (free at [console.groq.com](https://console.groq.com/keys))
- Optional: Google Search API key for better web search
- Optional: Bing Search API key (alternative to Google)

## 🚀 Quick Start

### 1. Get API Keys

1. **Groq API Key** (Required):
   - Visit [console.groq.com](https://console.groq.com/keys)
   - Create a free account
   - Generate an API key

2. **Google Search API** (Optional, for better web search):
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Custom Search API
   - Create credentials

### 2. Backend Setup

```bash
cd backend

# Windows users: run start.bat
# Linux/Mac users: run start.sh

# Or manual setup:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start the server
python app.py
```

### 3. Frontend Integration

Replace your current `script.js` with `script-rag.js` or update your HTML to use the new script:

```html
<!-- In index.html, replace the script reference -->
<script src="script-rag.js"></script>
```

### 4. Run the Application

1. Start the backend server: `python backend/app.py`
2. Open `static/index.html` in your browser
3. The frontend will automatically connect to the backend at `http://localhost:8000`

## 📂 Project Structure

```
Edu-Assist/
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── services/
│   │   ├── groq_service.py    # Groq API integration
│   │   ├── pdf_processor.py   # PDF processing and chunking
│   │   ├── vector_store.py    # Vector database operations
│   │   ├── web_search.py      # Web search functionality
│   │   └── rag_engine.py      # RAG orchestration
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── start.bat             # Windows startup script
│   └── start.sh              # Linux/Mac startup script
├── static/
│   ├── index.html            # Main chat interface
│   ├── script-rag.js         # Updated JavaScript with RAG integration
│   └── ... (other existing files)
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (for better web search)
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
BING_SEARCH_API_KEY=your_bing_api_key

# Database
DATABASE_PATH=vector_store.db

# Model settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Groq Models Available

- `llama3-8b-8192` (default)
- `llama3-70b-8192`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

## 📖 API Endpoints

### Chat
- `POST /api/chat` - Send a message and get AI response
- `GET /api/chat-history/{session_id}` - Get chat history

### Document Management
- `POST /api/upload-document` - Upload and process PDF
- `GET /api/documents` - List all uploaded documents
- `DELETE /api/documents/{doc_id}` - Delete a document

### Health & Status
- `GET /api/health` - Health check for all services
- `GET /docs` - Interactive API documentation (Swagger)

## 💡 Usage Examples

### 1. Basic Chat
```javascript
// Send a regular question
await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
        message: "Explain photosynthesis",
        subject: "Biology"
    })
});
```

### 2. Upload PDF and Query
```javascript
// Upload PDF
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('subject', 'Mathematics');
await fetch('/api/upload-document', { method: 'POST', body: formData });

// Ask question about the PDF
await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
        message: "What does the document say about quadratic equations?",
        subject: "Mathematics"
    })
});
```

### 3. ELI5 Mode
```javascript
// Ask for simple explanation
await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
        message: "How do computers work?",
        eli5_mode: true
    })
});
```

## 🛠️ Customization

### Modify Chunking Strategy
Edit `backend/services/pdf_processor.py`:

```python
def __init__(self):
    self.chunk_size = 1000      # Characters per chunk
    self.chunk_overlap = 200    # Overlap between chunks
```

### Change Embedding Model
Edit `backend/services/vector_store.py`:

```python
def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
    # Try other models:
    # - all-mpnet-base-v2 (higher quality, slower)
    # - distilbert-base-multilingual-cased (multilingual)
```

### Adjust RAG Parameters
Edit `backend/services/rag_engine.py`:

```python
def __init__(self, ...):
    self.similarity_threshold = 0.7    # Minimum similarity for chunks
    self.max_context_chunks = 3        # Max chunks to include
    self.max_web_results = 2           # Max web search results
```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **CORS errors in browser**
   - Make sure backend is running on port 8000
   - Check `allow_origins` in `app.py`

3. **Groq API errors**
   - Verify your API key in `.env`
   - Check rate limits (free tier: 30 requests/minute)

4. **PDF processing fails**
   ```bash
   pip install PyMuPDF
   ```

5. **Vector search not working**
   ```bash
   pip install sentence-transformers torch
   ```

### Debug Mode

Set `DEBUG=True` in `.env` for verbose logging.

## 📚 Dependencies

### Backend
- `fastapi` - Web framework
- `groq` - Groq API client
- `PyMuPDF` - PDF processing
- `sentence-transformers` - Text embeddings
- `numpy` - Numerical operations
- `aiohttp` - Async HTTP client
- `sqlite3` - Database (included with Python)

### Frontend
- Vanilla JavaScript (ES6+)
- Material Design Icons
- Your existing CSS framework

## 🔒 Security Notes

- Store API keys in `.env`, never commit them
- In production, restrict CORS origins
- Consider rate limiting for public deployments
- Validate file uploads and sizes

## 📈 Performance Tips

1. **Chunking**: Adjust chunk size based on your document types
2. **Embeddings**: Use GPU-enabled transformers for faster processing
3. **Caching**: Implement Redis for session and embedding caching
4. **Database**: Consider PostgreSQL with pgvector for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

- Create an issue for bugs or feature requests
- Check the `/api/health` endpoint for service status
- Review logs in the backend console for debugging

---

**Happy Learning with Edu Assist RAG! 🎓🤖**
