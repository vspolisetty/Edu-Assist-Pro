#!/usr/bin/env python3
# Updated: Edu Assist with dynamic Groq model support
"""
Test script to verify PDF processing setup
"""

import os
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_setup():
    """Check if the setup is ready for PDF processing"""
    print("🔍 Checking Edu Assist PDF Processing Setup...")
    print("=" * 50)
    
    # Check documents folder
    docs_path = Path("documents")
    if docs_path.exists():
        print("✅ Documents folder exists")
        
        # Check subfolders
        subjects = ["Math", "Science", "History", "General"]
        for subject in subjects:
            subject_path = docs_path / subject
            if subject_path.exists():
                pdf_count = len(list(subject_path.glob("*.pdf")))
                print(f"✅ {subject}/ folder exists ({pdf_count} PDFs)")
            else:
                print(f"❌ {subject}/ folder missing")
    else:
        print("❌ Documents folder not found")
        return False
    
    # Check required services
    try:
        from services.pdf_processor import PDFProcessor
        print("✅ PDF Processor service available")
    except ImportError as e:
        print(f"❌ PDF Processor import error: {e}")
        return False
    
    try:
        from services.vector_store import VectorStore
        print("✅ Vector Store service available")
    except ImportError as e:
        print(f"❌ Vector Store import error: {e}")
        return False
    
    # Check dependencies
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF (fitz) available")
    except ImportError:
        print("❌ PyMuPDF not installed. Run: pip install PyMuPDF")
        return False
    
    print("\n🎉 Setup verification complete!")
    print("\n📝 Next steps:")
    print("1. Add PDF files to the subject folders in documents/")
    print("2. Run: python bulk_process_pdfs.py")
    print("3. Start backend: python app.py")
    
    return True

def list_current_pdfs():
    """List all PDFs currently in the documents folder"""
    print("\n📚 Current PDFs in documents folder:")
    print("-" * 40)
    
    docs_path = Path("documents")
    total_pdfs = 0
    
    for subject_folder in docs_path.iterdir():
        if subject_folder.is_dir() and not subject_folder.name.startswith('.'):
            pdfs = list(subject_folder.glob("*.pdf"))
            total_pdfs += len(pdfs)
            
            print(f"\n📁 {subject_folder.name}/ ({len(pdfs)} PDFs)")
            for pdf in pdfs:
                size_mb = pdf.stat().st_size / (1024 * 1024)
                print(f"   📄 {pdf.name} ({size_mb:.1f} MB)")
    
    if total_pdfs == 0:
        print("   📭 No PDF files found")
        print("   💡 Add some PDF files to test the system!")
    else:
        print(f"\n📊 Total: {total_pdfs} PDF files ready for processing")

if __name__ == "__main__":
    if check_setup():
        list_current_pdfs()
        
        if input("\n🔄 Process all PDFs now? (y/n): ").lower() == 'y':
            print("\n🚀 Starting bulk processing...")
            os.system("python bulk_process_pdfs.py")
