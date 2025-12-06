from src.rag.advanced_rag import get_rag_instance

def query_rag_system(query: str, meeting_type: str = None, k: int = 5):
    """Query the RAG system."""
    try:
        rag = get_rag_instance()
        
        # We can implement a filter based on meeting_type if needed, 
        # but semantic_search handles it. 
        # Here we want to do QA (Smart Answer).
        
        # Or we can do simple semantic search if that's what the API expects.
        # But 'query_rag_system' implies getting an answer.
        # Let's use smart_qa.
        
        result = rag.smart_qa(query, context_k=k)
        return result.get('answer', 'No answer generated.')
        
    except Exception as e:
        return f"Error: {str(e)}"
