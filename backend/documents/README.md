# 📚 Edu Assist Documents Folder

This folder contains PDF documents that will be processed by the RAG system for educational content.

## 📁 Folder Structure

```
documents/
├── Math/           # Mathematics PDFs (algebra, calculus, geometry, etc.)
├── Science/        # Science PDFs (physics, chemistry, biology, etc.)
├── History/        # History PDFs (world history, local history, etc.)
└── General/        # General educational PDFs (study guides, etc.)
```

## 🚀 How to Use

1. **Add your PDFs** to the appropriate subject folders
2. **Run the bulk processor** to index them:
   ```bash
   python bulk_process_pdfs.py
   ```
3. **Start the backend server** to enable RAG functionality:
   ```bash
   python app.py
   ```

## 📝 File Organization Tips

- **Use descriptive filenames**: `algebra_basics.pdf`, `world_war_2_timeline.pdf`
- **Organize by subject**: Place files in the most relevant subject folder
- **Multiple subjects**: If a PDF covers multiple subjects, choose the primary one
- **File formats**: Only PDF files are supported currently

## 🔍 What Happens During Processing

1. **Text Extraction**: Content is extracted from each PDF
2. **Chunking**: Text is split into searchable segments
3. **Vector Storage**: Chunks are converted to embeddings for semantic search
4. **Subject Tagging**: Each chunk is tagged with its subject category

## ✅ Testing

After processing, you can test the system by:
- Asking questions related to your PDF content in the chat
- The AI will use your documents to provide accurate, contextual answers
- Responses will include information from the processed PDFs

---
*Generated on: August 15, 2025*
