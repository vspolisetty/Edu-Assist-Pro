# Updated: PDF processor with enhanced support
import fitz  # PyMuPDF
import re
import asyncio
from typing import List, Dict, Any
import hashlib
from datetime import datetime

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000  # Characters per chunk
        self.chunk_overlap = 200  # Overlap between chunks
    
    async def process_pdf(self, file_path: str, subject: str = "General") -> List[Dict[str, Any]]:
        """
        Process PDF file and return chunks of text
        """
        try:
            # Extract text from PDF
            text = await self._extract_text_from_pdf(file_path)
            
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Split into chunks
            chunks = self._create_chunks(cleaned_text)
            
            # Create chunk objects with metadata
            chunk_objects = []
            for i, chunk in enumerate(chunks):
                chunk_obj = {
                    "id": self._generate_chunk_id(file_path, i),
                    "text": chunk,
                    "metadata": {
                        "source": file_path,
                        "subject": subject,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "created_at": datetime.now().isoformat(),
                        "char_count": len(chunk),
                        "word_count": len(chunk.split())
                    }
                }
                chunk_objects.append(chunk_obj)
            
            return chunk_objects
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    async def _extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_extract_text, file_path)
    
    def _sync_extract_text(self, file_path: str) -> str:
        """
        Synchronous text extraction (runs in executor)
        """
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                # Extract text from the page
                page_text = page.get_text()  # type: ignore
                
                # Add page separator
                text += f"\\n--- Page {page_num + 1} ---\\n"
                text += page_text + "\\n"
            
            doc.close()
            return text
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and preprocess extracted text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page headers/footers patterns (common patterns)
        text = re.sub(r'--- Page \d+ ---', '', text)
        
        # Remove excessive line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove special characters that might interfere (but be more conservative)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        
        # Basic cleanup only
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        return text.strip()
    
    def _create_chunks(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Determine end position
            end = start + self.chunk_size
            
            if end >= len(text):
                # Last chunk
                chunks.append(text[start:])
                break
            
            # Try to break at a sentence boundary
            chunk_text = text[start:end]
            
            # Look for sentence endings within the last 200 characters
            sentence_endings = ['.', '!', '?']
            best_break = -1
            
            for i in range(len(chunk_text) - 1, max(len(chunk_text) - 200, 0), -1):
                if chunk_text[i] in sentence_endings and i + 1 < len(chunk_text) and chunk_text[i + 1] == ' ':
                    best_break = start + i + 1
                    break
            
            if best_break != -1:
                chunks.append(text[start:best_break].strip())
                start = best_break - self.chunk_overlap
            else:
                # Fallback: break at word boundary
                words = chunk_text.split()
                if len(words) > 1:
                    # Remove the last word to avoid cutting mid-word
                    chunk_text = ' '.join(words[:-1])
                
                chunks.append(chunk_text.strip())
                start = start + len(chunk_text) - self.chunk_overlap
            
            # Ensure we don't go backwards
            if start < 0:
                start = 0
        
        # Remove empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]
        
        return chunks
    
    def _generate_chunk_id(self, file_path: str, chunk_index: int) -> str:
        """
        Generate unique ID for chunk
        """
        source_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
        return f"chunk_{source_hash}_{chunk_index}"
    
    async def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF
        """
        try:
            loop = asyncio.get_event_loop()
            metadata = await loop.run_in_executor(None, self._sync_extract_metadata, file_path)
            return metadata
        except Exception as e:
            return {"error": str(e)}
    
    def _sync_extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Synchronous metadata extraction
        """
        try:
            doc = fitz.open(file_path)
            metadata = doc.metadata or {}
            
            pdf_info = {
                "title": metadata.get("title", "Unknown"),
                "author": metadata.get("author", "Unknown"),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", ""),
                "page_count": doc.page_count,
                "file_size": None  # Will be set by caller if needed
            }
            
            doc.close()
            return pdf_info
            
        except Exception as e:
            raise Exception(f"Error extracting PDF metadata: {str(e)}")
