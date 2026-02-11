#!/usr/bin/env python3
"""
Bulk PDF Processor for Edu Assist RAG System
Place your PDFs in the 'documents' folder and run this script to process them all.
"""

import os
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.pdf_processor import PDFProcessor
from services.vector_store import VectorStore

async def process_pdfs_in_folder(folder_path: str = "documents"):
    """Process all PDFs in the specified folder"""
    
    # Initialize services
    pdf_processor = PDFProcessor()
    vector_store = VectorStore()
    
    # Create folder if it doesn't exist
    documents_path = Path(folder_path)
    if not documents_path.exists():
        documents_path.mkdir()
        print(f"📁 Created {folder_path} directory")
        print(f"📝 Place your PDF files in: {documents_path.absolute()}")
        return
    
    # Find all PDF files
    pdf_files = list(documents_path.glob("**/*.pdf"))
    
    if not pdf_files:
        print(f"📂 No PDF files found in {folder_path}")
        print(f"📝 Place your PDF files in: {documents_path.absolute()}")
        return
    
    print(f"🔍 Found {len(pdf_files)} PDF files to process...")
    
    for pdf_file in pdf_files:
        try:
            print(f"📖 Processing: {pdf_file.name}")
            
            # Determine subject from folder structure
            relative_path = pdf_file.relative_to(documents_path)
            if len(relative_path.parts) > 1:
                subject = relative_path.parts[0]  # Use folder name as subject
            else:
                subject = "General"
            
            # Process PDF
            chunks = await pdf_processor.process_pdf(str(pdf_file), subject)
            
            # Store in vector database
            document_id = await vector_store.store_document_chunks(
                chunks=chunks,
                filename=pdf_file.name,
                subject=subject
            )
            
            print(f"✅ Successfully processed {pdf_file.name}")
            print(f"   📊 Subject: {subject}")
            print(f"   🔢 Chunks: {len(chunks)}")
            print(f"   🆔 Document ID: {document_id}")
            print()
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {str(e)}")
            print()
    
    print("🎉 Bulk processing complete!")

async def main():
    """Main function"""
    print("📚 Edu Assist PDF Bulk Processor")
    print("=" * 40)
    
    try:
        await process_pdfs_in_folder("documents")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
