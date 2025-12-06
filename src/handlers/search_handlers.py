"""Semantic search UI functions for Gradio integration."""

from typing import List, Tuple, Optional
from src.rag.advanced_rag import get_rag_instance

def search_meetings(
    query: str,
    meeting_type_filter: Optional[str] = None,
    language_filter: Optional[str] = None,
    n_results: int = 5
) -> Tuple[str, str]:
    """Search meetings using semantic search."""
    if not query or query.strip() == "":
        return "⚠️ Vui lòng nhập từ khóa tìm kiếm", ""
    
    try:
        rag = get_rag_instance()
        
        # Apply filters
        filter_metadata = {}
        if meeting_type_filter and meeting_type_filter != "Tất cả":
            filter_metadata["meeting_type"] = meeting_type_filter
            # Note: LangChain Chroma filter syntax might differ.
        if language_filter and language_filter != "Tất cả":
            filter_metadata["language"] = language_filter

        results = rag.semantic_search(
            query=query,
            k=n_results,
            filter_metadata=filter_metadata if filter_metadata else None
        )
        
        if not results:
            return "❌ Không tìm thấy kết quả phù hợp", ""
        
        # Format results
        markdown_output = []
        markdown_output.append(f"# 🔍 Tìm thấy {len(results)} kết quả\n")
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            
            markdown_output.append(f"## {i}. Meeting ID: {metadata.get('meeting_id', 'N/A')}")
            markdown_output.append(f"**Type:** {metadata.get('meeting_type', 'N/A')} | "
                                  f"**Language:** {metadata.get('language', 'N/A')} | "
                                  f"**Date:** {metadata.get('timestamp', 'N/A')[:10]}")
            
            # Show similarity score
            if result.get('score') is not None:
                # result['score'] might be distance or similarity depending on impl. 
                # Langchain usually returns distance for Chroma? 
                # But AdvancedRAG formatted it. Let's assume similarity or raw score.
                markdown_output.append(f"**Score:** {result['score']}")
            
            # Show transcript preview
            content = result.get('content', '')
            transcript_preview = content[:300] + "..." if content else "N/A"
            markdown_output.append(f"\n**Context Preview:**\n> {transcript_preview}\n")
            
            markdown_output.append("\n---\n")
        
        status = f"✅ Tìm thấy {len(results)} kết quả phù hợp"
        return status, "\n".join(markdown_output)
        
    except Exception as e:
        return f"❌ Lỗi: {str(e)}", ""


def get_vectordb_stats_ui() -> str:
    """Get vector DB statistics."""
    try:
        rag = get_rag_instance()
        stats = rag.get_stats()
        
        if stats.get('status') == 'error':
             return f"❌ Error: {stats.get('error')}"

        output = []
        output.append(f"# 📊 {stats.get('vector_store', 'DB').upper()} Statistics\n")
        output.append(f"**Total Records (Chunks):** {stats.get('total_meetings', 0)}\n")
        
        if stats.get('by_type'):
            output.append("**By Type:**")
            for mtype, count in stats['by_type'].items():
                output.append(f"- {mtype}: {count}")
            output.append("")
        
        if stats.get('by_language'):
            output.append("**By Language:**")
            for lang, count in stats['by_language'].items():
                output.append(f"- {lang}: {count}")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Alias for backward compatibility if needed, but we should update imports
get_vectordb_stats = get_vectordb_stats_ui 

def search_meetings_ui(query, meeting_type, language, n_results):
    """Wrapper for API usage."""
    return search_meetings(query, meeting_type, language, n_results)

def find_similar_to_meeting(meeting_id: str, n_results: int = 3) -> Tuple[str, str]:
    """Find meetings similar to a specific meeting."""
    # Assuming we can retrieve the meeting content first
    # But AdvancedRAG doesn't have a direct 'get_meeting' by ID easily unless we query.
    return "⚠️ Tính năng đang được cập nhật cho hệ thống RAG mới", ""
