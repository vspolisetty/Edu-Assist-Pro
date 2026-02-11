# Updated: Dynamic model support
from typing import Dict, List, Any, Optional
import asyncio
from services.groq_service import GroqService
from services.vector_store import VectorStore
from services.web_search import WebSearchService

class RAGEngine:
    def __init__(self, groq_service: GroqService, vector_store: VectorStore, web_search: WebSearchService):
        """
        Initialize RAG engine with required services
        """
        self.groq_service = groq_service
        self.vector_store = vector_store
        self.web_search = web_search
        
        # Configuration
        self.similarity_threshold = 0.7  # Minimum similarity score for relevant chunks
        self.max_context_chunks = 3      # Maximum number of chunks to use as context
        self.max_web_results = 2         # Maximum number of web search results to use
        self.context_max_chars = 2000    # Maximum characters for context
    
    async def get_response(
        self, 
        query: str, 
        subject: Optional[str] = None,
        eli5_mode: bool = False,
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Get AI response using RAG (Retrieval Augmented Generation)
        """
        try:
            # Step 1: Search for relevant chunks in vector store
            relevant_chunks = await self._search_knowledge_base(query, subject)
            
            # Step 2: If no relevant chunks found, search the web
            web_results = []
            if not relevant_chunks or all(chunk['similarity'] < self.similarity_threshold for chunk in relevant_chunks):
                web_results = await self._search_web(query)
            
            # Step 3: Build context from chunks and web results
            context = await self._build_context(relevant_chunks, web_results, query)
            
            # Step 4: Generate response using Groq
            response = await self.groq_service.generate_educational_response(
                query=query,
                context=context['text'],
                subject=subject or "General",
                eli5_mode=eli5_mode,
                chat_history=chat_history
            )
            
            return {
                'response': response,
                'sources': context['sources'],
                'context_type': context['type']
            }
            
        except Exception as e:
            # Fallback to direct response without context
            try:
                response = await self.groq_service.generate_educational_response(
                    query=query,
                    context="",
                    subject=subject or "General",
                    eli5_mode=eli5_mode,
                    chat_history=chat_history
                )
                
                return {
                    'response': response,
                    'sources': [],
                    'context_type': 'general_knowledge',
                    'note': 'Generated from general knowledge due to retrieval error'
                }
            except Exception as inner_e:
                return {
                    'response': f"I apologize, but I'm experiencing some technical difficulties. Could you please rephrase your question or try again in a moment? Error: {str(inner_e)}",
                    'sources': [],
                    'context_type': 'error'
                }
    
    async def _search_knowledge_base(self, query: str, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks in the vector store
        """
        try:
            return await self.vector_store.similarity_search(
                query=query,
                top_k=5,  # Get top 5 chunks initially
                subject_filter=subject
            )
        except Exception as e:
            print(f"Knowledge base search error: {e}")
            return []
    
    async def _search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the web for relevant information
        """
        try:
            # Make query more educational
            educational_query = f"{query} educational explanation tutorial"
            return await self.web_search.search(educational_query, num_results=self.max_web_results)
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    async def _build_context(self, chunks: List[Dict[str, Any]], web_results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """
        Build context from relevant chunks and web results
        """
        context_parts = []
        sources = []
        context_type = "none"
        
        # Add relevant chunks to context
        if chunks:
            context_type = "knowledge_base"
            relevant_chunks = [chunk for chunk in chunks[:self.max_context_chunks] 
                             if chunk['similarity'] >= self.similarity_threshold]
            
            if relevant_chunks:
                context_parts.append("From uploaded documents:")
                for i, chunk in enumerate(relevant_chunks, 1):
                    context_parts.append(f"\\n{i}. {chunk['text'][:500]}...")  # Limit chunk size
                    sources.append({
                        'type': 'document',
                        'source': chunk['filename'],
                        'similarity': chunk['similarity']
                    })
        
        # Add web search results if no good chunks found
        if not context_parts and web_results:
            context_type = "web_search"
            context_parts.append("From web search:")
            
            # Fetch content from top web results
            web_tasks = [self._get_web_content(result) for result in web_results]
            web_contents = await asyncio.gather(*web_tasks, return_exceptions=True)
            
            for i, (result, content) in enumerate(zip(web_results, web_contents), 1):
                if isinstance(content, str) and content.strip():
                    context_parts.append(f"\\n{i}. From {result['title']}: {content[:300]}...")
                    sources.append({
                        'type': 'web',
                        'source': result['title'],
                        'url': result['url']
                    })
        
        # If we have both, prioritize document chunks but mention web results
        elif context_parts and web_results:
            context_type = "hybrid"
            context_parts.append("\\n\\nAdditional web resources:")
            for result in web_results[:2]:  # Just add titles and URLs
                context_parts.append(f"- {result['title']}: {result['url']}")
                sources.append({
                    'type': 'web_reference',
                    'source': result['title'],
                    'url': result['url']
                })
        
        # Combine context and limit size
        context_text = "\\n".join(context_parts)
        if len(context_text) > self.context_max_chars:
            context_text = context_text[:self.context_max_chars] + "..."
        
        return {
            'text': context_text,
            'sources': sources,
            'type': context_type
        }
    
    async def _get_web_content(self, result: Dict[str, Any]) -> str:
        """
        Get content from a web search result
        """
        try:
            # First try to use the snippet
            snippet = result.get('snippet', '').strip()
            if snippet:
                return snippet
            
            # If no snippet or short snippet, try to fetch page content
            if len(snippet) < 100 and result.get('url'):
                page_content = await self.web_search.get_page_content(result['url'], max_chars=500)
                return page_content if page_content else snippet
            
            return snippet
            
        except Exception as e:
            print(f"Error getting web content: {e}")
            return result.get('snippet', '')
    
    async def process_follow_up(self, query: str, previous_context: str, chat_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process follow-up questions with previous context
        """
        # For follow-up questions, we can reuse previous context and add new search if needed
        enhanced_query = f"Follow-up question: {query}\\nPrevious context: {previous_context[:500]}"
        
        # Search for additional relevant information
        new_chunks = await self._search_knowledge_base(enhanced_query)
        
        # Build context including previous context
        context = {
            'text': f"Previous context: {previous_context[:500]}\\n\\nAdditional information: {new_chunks[0]['text'] if new_chunks else 'None found'}",
            'sources': [],
            'type': 'follow_up'
        }
        
        response = await self.groq_service.generate_educational_response(
            query=query,
            context=context['text'],
            subject="General",
            eli5_mode=False,
            chat_history=chat_history
        )
        
        return {
            'response': response,
            'sources': context['sources'],
            'context_type': context['type']
        }
