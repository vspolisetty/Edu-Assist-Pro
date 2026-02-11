# 🤖 Edu Assist RAG Integration - Quick Setup

This integrates RAG (AI document search) into your **existing working website** without breaking anything!

## 🎯 What This Does

- **Keeps everything working** - Your website works exactly as before
- **Adds PDF upload** - Upload study materials via the attach button  
- **Smarter responses** - AI searches your documents first, then the web
- **Graceful fallback** - If backend is down, uses your original responses
- **Zero breaking changes** - Your existing features remain untouched

## ⚡ Quick Start (5 minutes)

### 1. Get Groq API Key (Free)
```
1. Go to: https://console.groq.com/keys  
2. Sign up (free)
3. Create API key
4. Copy it
```

### 2. Setup Backend
```bash
cd backend

# Check if you have everything needed
python check_setup.py

# Windows: Double-click start.bat
# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Add your API key to .env file:
GROQ_API_KEY=your_actual_key_here

# Start backend
python app.py
```

### 3. Test Your Website
```
1. Open your static/index.html (same as before)
2. Look for small 🧠 icon in logo (means RAG is connected)  
3. Try uploading a PDF with the attach button
4. Ask questions about your PDF!
```

## 🔧 How It Works

### Normal Operation (Backend Off)
- **Everything works exactly as before**
- Uses your existing `generateAIResponse()` method
- No changes to user experience

### Enhanced Mode (Backend On)  
- **PDF Upload**: Attach button uploads PDFs
- **Smart Search**: Searches your documents first
- **Source Citations**: Shows where answers came from  
- **Web Fallback**: Searches web if no documents match

## 🚨 Troubleshooting

### "Backend not connecting"
- Your website still works normally!
- Check if `python app.py` is running
- Visit http://localhost:8000/health to test

### "Import errors"
```bash
pip install -r requirements.txt
```

### "API key errors"
- Edit `backend/.env` file
- Add: `GROQ_API_KEY=your_real_key`

## 📁 Files Added (Your originals untouched)

```
static/
├── index.html (minimal change - added 1 script line)
├── script.js (minimal change - exposed instance)
├── rag-integration.js (NEW - optional enhancement)
└── ... (all your existing files unchanged)

backend/ (NEW folder)
├── app.py (FastAPI server)
├── services/ (RAG logic)
├── requirements.txt
├── .env (your API key)
└── start.bat / start.sh
```

## 🎮 Usage Examples

### Upload PDF and Ask Questions
1. Click attach button → select PDF
2. Wait for "processed" message  
3. Ask: "What does the document say about...?"

### Normal Chat (works as before)
1. Type any question
2. Get AI response (enhanced with document knowledge if available)

### ELI5 Mode (enhanced)  
1. Toggle ELI5 mode
2. Get simplified explanations from documents + web

## 💡 Pro Tips

- **Start simple**: Just get the backend running, everything else is automatic
- **PDF quality**: Better formatted PDFs = better answers
- **Subject matching**: Upload PDFs for the subject you're studying
- **Fallback ready**: If backend fails, website continues normally

---

**Your website works perfectly as-is. This just makes it smarter! 🧠**
