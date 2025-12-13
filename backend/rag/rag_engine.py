"""
RAG Engine for Meeting History.

This module implements the Retrieval-Augmented Generation logic:
1. Retrieve relevant contexts from ChromaDB (via HistorySearcher).
2. Construct a prompt with context.
3. Generate answer using LLM.

Enhanced with:
- Conversation Memory (multi-turn context)
- Query Expansion (LLM-powered query improvement)
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

from backend.data.history_searcher import HistorySearcher
from backend.llm.factory import LLMFactory
from backend.llm.prompts import PromptTemplates

load_dotenv()

class RAGEngine:
    """Engine for chatting with meeting history."""
    
    def __init__(self):
        """Initialize RAG Engine."""
        self.searcher = HistorySearcher()
        self.llm = self._init_llm()
        
    def _init_llm(self):
        """Initialize LLM from factory."""
        # Prioritize Gemini for speed/cost, then OpenAI
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key:
            return LLMFactory.create("gemini", api_key=gemini_key)
        elif openai_key:
            return LLMFactory.create("openai", api_key=openai_key)
        else:
            print("[RAGEngine] Warning: No API Key found. Chat will not work.")
            return None

    def _expand_query(self, query: str, conversation_context: str = "") -> str:
        """
        Expand and improve the user query using LLM.
        
        Args:
            query: Original user question
            conversation_context: Previous conversation history
            
        Returns:
            Expanded query string
        """
        if not self.llm:
            return query
            
        expansion_prompt = f"""You are a query expansion expert. 
Your task is to rewrite the user's question to be more specific and searchable for a semantic search system.

{conversation_context}

Current question: "{query}"

Rewrite this question to:
1. Include relevant context from previous conversation (if any)
2. Be more specific and detailed
3. Include important entities, dates, or keywords
4. Maintain the original intent

Return ONLY the rewritten question, nothing else.

Rewritten question:"""

        try:
            expanded = self.llm.generate(expansion_prompt).strip()
            print(f"[RAGEngine] Query expanded: '{query}' -> '{expanded}'")
            return expanded
        except Exception as e:
            print(f"[RAGEngine] Query expansion failed: {e}")
            return query

    def chat(self, query: str, conversation_history: List[Dict] = None, top_k: int = 5) -> Dict:
        """
        Answer a user question based on meeting history with conversation memory.
        
        Args:
            query: User question
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict containing 'answer' and 'sources'
        """
        if not self.llm:
            return {
                "answer": "AI service is not configured (missing API Key).",
                "sources": []
            }
        
        # Format conversation context
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            context_lines = ["Previous conversation:"]
            for msg in conversation_history[-10:]:  # Last 5 turns (10 messages)
                role_label = "User" if msg["role"] == "user" else "AI"
                context_lines.append(f"{role_label}: {msg['content']}")
            conversation_context = "\n".join(context_lines)
            
        # Step 1: Expand Query
        expanded_query = self._expand_query(query, conversation_context)
        
        # Step 2: Retrieve relevant documents
        print(f"[RAGEngine] Retrieving for: {expanded_query}")
        search_results = self.searcher.semantic_search(expanded_query, top_k=top_k)
        
        if not search_results:
            return {
                "answer": "I couldn't find any relevant meetings in your history to answer that.",
                "sources": []
            }
            
        # Step 3: Construct Context
        context_parts = []
        sources = []
        
        for i, res in enumerate(search_results):
            meta = res.get('metadata', {})
            source_name = meta.get('original_file', f"Meeting {i+1}")
            text = res.get('matched_text', '')
            score = res.get('score', 0)
            
            # Add to context
            context_parts.append(f"SOURCE [{i+1}] ({source_name}):\n{text}\n")
            
            # Add to sources list
            sources.append({
                "id": i+1,
                "name": source_name,
                "score": score,
                "timestamp": meta.get('timestamp')
            })
            
        full_context = "\n".join(context_parts)
        
        # Step 4: Construct Prompt with Conversation History
        prompt_parts = [
            "You are an intelligent assistant helping a user extract information from their meeting history.",
            ""
        ]
        
        # Add conversation context if exists
        if conversation_context:
            prompt_parts.append(conversation_context)
            prompt_parts.append("")
        
        prompt_parts.extend([
            f'USER QUESTION: "{query}"',
            "",
            "Answer the question strictly based on the following retrieved meeting contexts.",
            "If the answer is not in the context, say so.",
            "Cite your sources using [1], [2] notation where appropriate.",
            "If the question references previous conversation, use that context to provide a complete answer.",
            "",
            "=== RETRIEVED CONTEXTS ===",
            full_context,
            "==========================",
            "",
            "ANSWER:"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        # Step 5: Generate Answer
        print("[RAGEngine] Generating answer...")
        answer = self.llm.generate(prompt)
        
        return {
            "answer": answer.strip(),
            "sources": sources,
            "expanded_query": expanded_query  # For debugging
        }
    
    def chat_stream(self, query: str, conversation_history: List[Dict] = None, top_k: int = 5):
        """Stream answer for user question based on meeting history.
        
        Args:
            query: User question
            conversation_history: List of previous messages
            top_k: Number of chunks to retrieve
            
        Yields:
            JSON strings with either 'chunk', 'sources', or 'error' keys
        """
        import json
        
        if not self.llm:
            yield json.dumps({"error": "AI service is not configured"})
            return
        
        # Same retrieval logic as chat()
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            context_lines = ["Previous conversation:"]
            for msg in conversation_history[-10:]:
                role_label = "User" if msg["role"] == "user" else "AI"
                context_lines.append(f"{role_label}: {msg['content']}")
            conversation_context = "\n".join(context_lines)
        
        expanded_query = self._expand_query(query, conversation_context)
        print(f"[RAGEngine] Streaming for: {expanded_query}")
        
        search_results = self.searcher.semantic_search(expanded_query, top_k=top_k)
        
        if not search_results:
            yield json.dumps({"error": "No relevant meetings found"})
            return
        
        # Build context and sources
        context_parts = []
        sources = []
        
        for i, res in enumerate(search_results):
            meta = res.get('metadata', {})
            source_name = meta.get('original_file', f"Meeting {i+1}")
            text = res.get('matched_text', '')
            score = res.get('score', 0)
            
            context_parts.append(f"SOURCE [{i+1}] ({source_name}):\n{text}\n")
            sources.append({
                "id": i+1,
                "name": source_name,
                "score": score,
                "timestamp": meta.get('timestamp')
            })
        
        # Send sources first
        yield json.dumps({"sources": sources, "expanded_query": expanded_query})
        
        # Build prompt
        full_context = "\n".join(context_parts)
        prompt_parts = [
            "You are an intelligent assistant helping a user extract information from their meeting history.",
            ""
        ]
        
        if conversation_context:
            prompt_parts.append(conversation_context)
            prompt_parts.append("")
        
        prompt_parts.extend([
            f'USER QUESTION: "{query}"',
            "",
            "Answer the question strictly based on the following retrieved meeting contexts.",
            "If the answer is not in the context, say so.",
            "Cite your sources using [1], [2] notation where appropriate.",
            "If the question references previous conversation, use that context to provide a complete answer.",
            "",
            "=== RETRIEVED CONTEXTS ===",
            full_context,
            "==========================",
            "",
            "ANSWER:"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        # Stream answer
        print("[RAGEngine] Streaming answer...")
        try:
            for chunk in self.llm.generate_stream(prompt):
                yield json.dumps({"chunk": chunk})
        except Exception as e:
            yield json.dumps({"error": str(e)})

