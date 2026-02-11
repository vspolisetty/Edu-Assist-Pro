# Updated: Vector store with dynamic model support
import numpy as np
import asyncio
import sqlite3
import json
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
from sentence_transformers import SentenceTransformer
import os

class VectorStore:
    def __init__(self, db_path: str = "vector_store.db", model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector store with SQLite database and sentence transformer
        """
        self.db_path = db_path
        self.model_name = model_name
        self.embedding_model: Optional[SentenceTransformer] = None
        self.embedding_dimension = 384  # Default for all-MiniLM-L6-v2
        
        # Initialize database synchronously
        self._sync_init_db()
    
    async def _init_db(self):
        """
        Initialize SQLite database with required tables
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._sync_init_db)
    
    def _sync_init_db(self):
        """
        Synchronous database initialization
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                subject TEXT NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Create chunks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                text TEXT NOT NULL,
                embedding BLOB,
                metadata TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_subject ON documents(subject)')
        
        conn.commit()
        conn.close()
    
    async def _load_embedding_model(self):
        """
        Load sentence transformer model
        """
        if self.embedding_model is None:
            loop = asyncio.get_event_loop()
            self.embedding_model = await loop.run_in_executor(
                None, 
                lambda: SentenceTransformer(self.model_name)
            )
    
    async def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        """
        await self._load_embedding_model()
        if self.embedding_model is None:
            raise Exception("Failed to load embedding model")
        
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            lambda: self.embedding_model.encode(texts, convert_to_numpy=True)  # type: ignore
        )
        return embeddings
    
    async def store_document_chunks(self, chunks: List[Dict[str, Any]], filename: str, subject: str) -> str:
        """
        Store document chunks in vector database
        """
        try:
            # Generate document ID
            document_id = str(uuid.uuid4())
            
            # Extract text for embedding generation
            texts = [chunk['text'] for chunk in chunks]
            
            # Generate embeddings
            embeddings = await self.generate_embeddings(texts)
            
            # Store in database
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, 
                self._sync_store_chunks, 
                document_id, filename, subject, chunks, embeddings
            )
            
            return document_id
            
        except Exception as e:
            raise Exception(f"Error storing document chunks: {str(e)}")
    
    def _sync_store_chunks(self, document_id: str, filename: str, subject: str, 
                          chunks: List[Dict[str, Any]], embeddings: np.ndarray):
        """
        Synchronous chunk storage
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Store document metadata
            cursor.execute('''
                INSERT INTO documents (id, filename, subject, created_at, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                document_id,
                filename,
                subject,
                datetime.now().isoformat(),
                json.dumps({"chunk_count": len(chunks)})
            ))
            
            # Store chunks with embeddings
            for i, chunk in enumerate(chunks):
                embedding_blob = embeddings[i].tobytes()
                
                cursor.execute('''
                    INSERT INTO chunks (id, document_id, chunk_index, text, embedding, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    chunk['id'],
                    document_id,
                    i,
                    chunk['text'],
                    embedding_blob,
                    json.dumps(chunk.get('metadata', {})),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    async def similarity_search(self, query: str, top_k: int = 5, subject_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform similarity search for relevant chunks
        """
        try:
            # Generate query embedding
            query_embeddings = await self.generate_embeddings([query])
            query_embedding = query_embeddings[0]
            
            # Search database
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                self._sync_similarity_search,
                query_embedding,
                top_k,
                subject_filter
            )
            
            return results
            
        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")
    
    def _sync_similarity_search(self, query_embedding: np.ndarray, top_k: int, 
                               subject_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Synchronous similarity search
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Build query with optional subject filter
            if subject_filter:
                cursor.execute('''
                    SELECT c.id, c.text, c.embedding, c.metadata, d.filename, d.subject
                    FROM chunks c
                    JOIN documents d ON c.document_id = d.id
                    WHERE d.subject = ?
                ''', (subject_filter,))
            else:
                cursor.execute('''
                    SELECT c.id, c.text, c.embedding, c.metadata, d.filename, d.subject
                    FROM chunks c
                    JOIN documents d ON c.document_id = d.id
                ''')
            
            rows = cursor.fetchall()
            
            if not rows:
                return []
            
            # Calculate similarities
            similarities = []
            for row in rows:
                chunk_id, text, embedding_blob, metadata, filename, subject = row
                
                # Convert blob back to numpy array
                chunk_embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                chunk_embedding = chunk_embedding.reshape(1, -1)
                query_embedding_reshaped = query_embedding.reshape(1, -1)
                
                # Calculate cosine similarity
                similarity = np.dot(query_embedding_reshaped, chunk_embedding.T)[0][0]
                
                similarities.append({
                    'chunk_id': chunk_id,
                    'text': text,
                    'similarity': float(similarity),
                    'metadata': json.loads(metadata) if metadata else {},
                    'filename': filename,
                    'subject': subject
                })
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            raise e
        finally:
            conn.close()
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all stored documents
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_list_documents)
    
    def _sync_list_documents(self) -> List[Dict[str, Any]]:
        """
        Synchronous document listing
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT d.id, d.filename, d.subject, d.created_at, d.metadata, COUNT(c.id) as chunk_count
                FROM documents d
                LEFT JOIN chunks c ON d.id = c.document_id
                GROUP BY d.id, d.filename, d.subject, d.created_at, d.metadata
                ORDER BY d.created_at DESC
            ''')
            
            rows = cursor.fetchall()
            documents = []
            
            for row in rows:
                doc_id, filename, subject, created_at, metadata, chunk_count = row
                documents.append({
                    'id': doc_id,
                    'filename': filename,
                    'subject': subject,
                    'created_at': created_at,
                    'metadata': json.loads(metadata) if metadata else {},
                    'chunk_count': chunk_count
                })
            
            return documents
            
        except Exception as e:
            raise e
        finally:
            conn.close()
    
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document and all its chunks
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_delete_document, document_id)
    
    def _sync_delete_document(self, document_id: str) -> bool:
        """
        Synchronous document deletion
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete chunks first
            cursor.execute('DELETE FROM chunks WHERE document_id = ?', (document_id,))
            
            # Delete document
            cursor.execute('DELETE FROM documents WHERE id = ?', (document_id,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            return deleted_count > 0
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    async def health_check(self) -> bool:
        """
        Check if vector store is working
        """
        try:
            await self._load_embedding_model()
            # Test embedding generation
            test_embeddings = await self.generate_embeddings(["test"])
            return test_embeddings is not None and len(test_embeddings) > 0
        except:
            return False
