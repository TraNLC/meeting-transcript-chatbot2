"""Semantic search UI functions for Gradio integration."""

from typing import List, Tuple, Optional
from .chroma_manager import ChromaManager


def search_meetings(
    query: str,
    meeting_type_filter: Optional[str] = None,
    language_filter: Optional[str] = None,
    n_results: int = 5
) -> Tuple[str, str]:
    """Search meetings using semantic search.
    
    Args:
        query: Search query
        meeting_type_filter: Filter by meeting type
        language_filter: Filter by language
        n_results: Number of results
        
    Returns:
        Tuple of (status_message, results_markdown)
    """
    if not query or query.strip() == "":
        return "⚠️ Vui lòng nhập từ khóa tìm kiếm", ""
    
    try:
        chroma = ChromaManager()
        
        # Apply filters
        mt_filter = meeting_type_filter if meeting_type_filter != "All" else None
        lang_filter = language_filter if language_filter != "All" else None
        
        results = chroma.semantic_search(
            query=query,
            n_results=n_results,
            meeting_type=mt_filter,
            language=lang_filter
        )
        
        if not results:
            return "❌ Không tìm thấy kết quả phù hợp", ""
        
        # Format results
        markdown_output = []
        markdown_output.append(f"# 🔍 Tìm thấy {len(results)} kết quả\n")
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            analysis = result.get('analysis', {})
            
            markdown_output.append(f"## {i}. Meeting ID: {result['meeting_id']}")
            markdown_output.append(f"**Type:** {metadata.get('meeting_type', 'N/A')} | "
                                  f"**Language:** {metadata.get('language', 'N/A')} | "
                                  f"**Date:** {metadata.get('timestamp', 'N/A')[:10]}")
            
            # Show similarity score
            if result.get('distance') is not None:
                similarity = max(0, 100 - result['distance'] * 100)
                markdown_output.append(f"**Similarity:** {similarity:.1f}%")
            
            # Show transcript preview
            transcript_preview = result['transcript'][:300] + "..."
            markdown_output.append(f"\n**Transcript Preview:**\n> {transcript_preview}\n")
            
            # Show key findings
            if analysis:
                markdown_output.append("**Key Findings:**")
                
                # Participants
                participants = analysis.get('get_meeting_participants', {}).get('result', {}).get('participants', [])
                if participants:
                    markdown_output.append(f"- 👥 Participants: {', '.join(participants[:3])}")
                
                # Action items
                action_items = analysis.get('extract_action_items', {}).get('result', {}).get('action_items', [])
                if action_items:
                    markdown_output.append(f"- ✅ Action Items: {len(action_items)}")
                
                # Decisions
                decisions = analysis.get('extract_decisions', {}).get('result', {}).get('decisions', [])
                if decisions:
                    markdown_output.append(f"- 📋 Decisions: {len(decisions)}")
                
                # Workshop-specific
                if metadata.get('meeting_type') == 'workshop':
                    key_learnings = analysis.get('extract_key_learnings', {}).get('result', {}).get('key_learnings', [])
                    if key_learnings:
                        markdown_output.append(f"- 📚 Key Learnings: {len(key_learnings)}")
            
            markdown_output.append("\n---\n")
        
        status = f"✅ Tìm thấy {len(results)} meetings phù hợp với '{query}'"
        return status, "\n".join(markdown_output)
        
    except Exception as e:
        return f"❌ Lỗi: {str(e)}", ""


def get_vectordb_stats() -> str:
    """Get ChromaDB statistics.
    
    Returns:
        Markdown formatted statistics
    """
    try:
        chroma = ChromaManager()
        stats = chroma.get_statistics()
        
        output = []
        output.append("# 📊 ChromaDB Statistics\n")
        output.append(f"**Total Meetings:** {stats['total_meetings']}\n")
        
        if stats['by_type']:
            output.append("**By Type:**")
            for mtype, count in stats['by_type'].items():
                output.append(f"- {mtype}: {count}")
            output.append("")
        
        if stats['by_language']:
            output.append("**By Language:**")
            for lang, count in stats['by_language'].items():
                output.append(f"- {lang}: {count}")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def find_similar_to_meeting(meeting_id: str, n_results: int = 3) -> Tuple[str, str]:
    """Find meetings similar to a specific meeting.
    
    Args:
        meeting_id: Reference meeting ID
        n_results: Number of similar meetings to find
        
    Returns:
        Tuple of (status_message, results_markdown)
    """
    if not meeting_id or meeting_id.strip() == "":
        return "⚠️ Vui lòng nhập Meeting ID", ""
    
    try:
        chroma = ChromaManager()
        results = chroma.find_similar_meetings(meeting_id, n_results=n_results)
        
        if not results:
            return "❌ Không tìm thấy meetings tương tự", ""
        
        # Format results (similar to search_meetings)
        markdown_output = []
        markdown_output.append(f"# 🔗 Tìm thấy {len(results)} meetings tương tự\n")
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            markdown_output.append(f"## {i}. Meeting ID: {result['meeting_id']}")
            markdown_output.append(f"**Type:** {metadata.get('meeting_type', 'N/A')} | "
                                  f"**Language:** {metadata.get('language', 'N/A')}")
            
            if result.get('distance') is not None:
                similarity = max(0, 100 - result['distance'] * 100)
                markdown_output.append(f"**Similarity:** {similarity:.1f}%")
            
            markdown_output.append("\n---\n")
        
        status = f"✅ Tìm thấy {len(results)} meetings tương tự"
        return status, "\n".join(markdown_output)
        
    except Exception as e:
        return f"❌ Lỗi: {str(e)}", ""
