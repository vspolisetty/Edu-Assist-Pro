# 🎓 Edu Assist RAG Educational Platform

## 🚀 Quick Start

### Option 1: Double-click to launch
1. **Double-click** `Start_Edu_Assist.bat`
2. **Wait** for the servers to start
3. **Browser opens automatically** at `http://localhost:3000`

### Option 2: Command line
```bash
python simple_launch.py
```

## 🌐 Access URLs

Once running, access these URLs:

- **🏠 Main Platform**: http://localhost:3000/static/
- **📚 Login Page**: http://localhost:3000/static/login.html  
- **📊 Dashboard**: http://localhost:3000/static/dashboard.html
- **💬 Chat Interface**: http://localhost:3000/static/index.html
- **🔍 API Health**: http://localhost:3000/health

## 📋 How to Test

1. **Open** http://localhost:3000/static/login.html
2. **Login** with any credentials (demo mode)
3. **Navigate** to the chat interface
4. **Ask questions** about your PDF content:
   - "Explain algebra concepts"
   - "What are Newton's laws?"
   - "Help me with calculus"

## 📚 Your PDF Knowledge Base

The system includes:
- **Math Textbook.pdf** (840 text chunks)
- **Science Text.pdf** (926 text chunks)
- **Total**: 1,766 searchable segments

## 🛠️ Troubleshooting

- **Port in use?** The system runs on port 3000
- **PDF not working?** Check `backend/documents/` folder
- **API errors?** Verify backend server started successfully

## 🔧 System Requirements

- Python 3.8+
- All dependencies in `backend/requirements.txt`
- Groq API key configured in `backend/.env`

---
*🤖 Powered by Groq AI + RAG Technology*
