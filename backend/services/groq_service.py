# Updated: Dynamic model fetching from Groq API
import os
from groq import Groq
import asyncio
from typing import List, Dict, Optional, Any
import aiohttp

class GroqService:
    def __init__(self):
        """
        Initialize Groq client with API key from environment variables
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.default_model = None  # Will be set dynamically
        self._available_models = None
        
    async def get_available_models(self) -> List[str]:
        """
        Fetch available models from Groq API
        """
        if self._available_models is not None:
            return self._available_models
            
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with session.get("https://api.groq.com/openai/v1/models", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [model['id'] for model in data.get('data', [])]
                        self._available_models = models
                        print(f"✅ Available Groq models: {models}")
                        return models
                    else:
                        print(f"⚠️ Failed to fetch models: {response.status}")
                        return []
        except Exception as e:
            print(f"⚠️ Error fetching models: {e}")
            return []
    
    async def get_default_model(self) -> str:
        """
        Get the best available model from Groq, preferring well-known ones.
        """
        # Preferred models in order of preference (current as of 2025/2026)
        PREFERRED = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ]
        if self.default_model is None:
            models = await self.get_available_models()
            # Pick the first preferred model that's actually available
            chosen = None
            for pref in PREFERRED:
                if pref in models:
                    chosen = pref
                    break
            if not chosen and models:
                chosen = models[0]
            self.default_model = chosen or "llama-3.3-70b-versatile"
            print(f"✅ Using default model: {self.default_model}")
        return self.default_model
        
    async def chat_completion(
        self, 
        messages: List[Dict[str, Any]], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Generate chat completion using Groq API
        """
        try:
            # Get the model to use (dynamic or provided)
            model_to_use = model or await self.get_default_model()
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model_to_use,
                    messages=messages,  # type: ignore
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    async def generate_educational_response(
        self,
        query: str,
        context: str = "",
        subject: str = "General",
        eli5_mode: bool = False,
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate educational response with context and subject-specific formatting
        """
        # Build the system prompt for educational context
        system_prompt = self._build_educational_system_prompt(subject, eli5_mode)
        
        # Build messages array
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history for context (last few messages)
        if chat_history:
            for msg in chat_history[-5:]:  # Last 5 messages
                if msg.get("role") in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
        
        # Add current query with context
        user_message = self._format_user_message(query, context)
        messages.append({"role": "user", "content": user_message})
        
        return await self.chat_completion(
            messages=messages,
            temperature=0.7 if not eli5_mode else 0.8,
            max_tokens=1500
        )
    
    def _build_educational_system_prompt(self, subject: str, eli5_mode: bool) -> str:
        """
        Build system prompt for educational chatbot
        """
        base_prompt = f"""You are an educational AI assistant for VoxTech Learning Platform, designed to teach 10th grade students about {subject}.

Your role is to provide clear, educational responses as a patient teacher who explains concepts step-by-step.

TEACHING STYLE FOR 10TH GRADERS:
- Explain concepts as if you're a friendly teacher in a classroom
- Break down complex ideas into simple, easy-to-understand steps
- Use encouraging language and relatable examples
- Start with basic concepts before moving to advanced ones
- Ask rhetorical questions to engage thinking: "Now, why do you think this works?"
- Use phrases like "Let's think about this together" or "Here's a helpful way to remember this"

FORMATTING REQUIREMENTS:
- Use clear paragraphs separated by double line breaks
- Use bullet points (•) for step-by-step explanations
- Use **bold text** for key vocabulary and important concepts
- Structure responses like a mini-lesson with clear sections
- Always end with an encouraging note or summary

RESPONSE STRUCTURE:
**Introduction**
Brief, encouraging explanation of what we're going to learn.

**Key Concepts:**
• Important point 1 with clear explanation
• Important point 2 with clear explanation
• Important point 3 with clear explanation

**Step-by-Step Example:**
Walk through a problem or concept step by step.

**Summary**
Encouraging wrap-up that reinforces learning.

You are a helpful educational teacher who can explain any topic clearly and thoroughly."""
        
        if eli5_mode:
            base_prompt += """
        
        IMPORTANT: ELI5 MODE is ON. Explain everything as if talking to a 5-year-old:
        - Use very simple words and short sentences
        - Use fun analogies and comparisons to everyday objects
        - Be extra patient and encouraging
        - Avoid technical jargon completely
        - Use emojis to make it more engaging
        - Still maintain proper formatting with line breaks and structure
        """
        
        return base_prompt
    
    def _format_user_message(self, query: str, context: str) -> str:
        """
        Format user message with context if available
        """
        if context.strip():
            return f"""I have some relevant information from my knowledge base:

{context}

Please answer this question as a teacher for 10th grade students: {query}

Use the provided information if relevant, but feel free to expand with additional teaching points to help explain the concept thoroughly."""
        else:
            return f"""Please answer this question as a teacher for 10th grade students: {query}

Explain the concept clearly and thoroughly to help them understand."""
    
    async def health_check(self) -> bool:
        """
        Check if Groq service is working
        """
        try:
            test_messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello' if you're working."}
            ]
            response = await self.chat_completion(test_messages, max_tokens=10)
            return "Hello" in response or "hello" in response.lower()
        except:
            return False
