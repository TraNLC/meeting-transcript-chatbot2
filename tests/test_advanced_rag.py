"""
Test Advanced RAG Features

Tests:
1. Conversation Memory - Multi-turn Q&A
2. Query Expansion - LLM-powered query improvement
3. Basic Chat - Standard RAG functionality
"""

import sys
from pathlib import Path

# Ensure backend imports work
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.rag.rag_engine import RAGEngine
    from backend.rag.conversation_manager import get_conversation_manager
    import uuid
    
    print("=" * 60)
    print("ADVANCED RAG BACKEND TEST")
    print("=" * 60)
    
    # Initialize
    engine = RAGEngine()
    conv_manager = get_conversation_manager()
    session_id = str(uuid.uuid4())
    
    print(f"\nTest Session ID: {session_id}")
    print("\n" + "-" * 60)
    
    # TEST 1: Basic Chat (No History)
    print("\n[TEST 1] Basic Chat - No Conversation History")
    print("-" * 60)
    
    query1 = "What meetings discussed budget or financial planning?"
    print(f"\nQuery: {query1}")
    
    response1 = engine.chat(query1, conversation_history=[])
    print(f"\nExpanded Query: {response1.get('expanded_query', 'N/A')}")
    print(f"\nAnswer:\n{response1['answer']}")
    print(f"\nSources: {len(response1['sources'])} found")
    for src in response1['sources'][:3]:
        print(f"  - {src['name']} (Score: {src['score']:.2f})")
    
    # Save to conversation
    conv_manager.add_message(session_id, "user", query1)
    conv_manager.add_message(session_id, "assistant", response1['answer'])
    
    print("\n" + "-" * 60)
    
    # TEST 2: Conversation Memory - Follow-up Question
    print("\n[TEST 2] Conversation Memory - Follow-up Question")
    print("-" * 60)
    
    query2 = "Who was assigned to handle this?"  # Relies on context from Q1
    print(f"\nQuery: {query2}")
    print("(This should understand 'this' refers to previous question)")
    
    history = conv_manager.get_history(session_id)
    print(f"\nConversation History: {len(history)} messages")
    
    response2 = engine.chat(query2, conversation_history=history)
    print(f"\nExpanded Query: {response2.get('expanded_query', 'N/A')}")
    print(f"\nAnswer:\n{response2['answer']}")
    print(f"\nSources: {len(response2['sources'])} found")
    
    # Save to conversation
    conv_manager.add_message(session_id, "user", query2)
    conv_manager.add_message(session_id, "assistant", response2['answer'])
    
    print("\n" + "-" * 60)
    
    # TEST 3: Query Expansion Demonstration
    print("\n[TEST 3] Query Expansion - Vague Query")
    print("-" * 60)
    
    query3 = "marketing stuff"  # Very vague
    print(f"\nOriginal Query: '{query3}' (intentionally vague)")
    
    history = conv_manager.get_history(session_id)
    response3 = engine.chat(query3, conversation_history=history)
    
    print(f"\nExpanded Query: '{response3.get('expanded_query', 'N/A')}'")
    print("^ Notice how the query is improved!")
    print(f"\nAnswer:\n{response3['answer']}")
    print(f"\nSources: {len(response3['sources'])} found")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)
    
    # Display Full Conversation
    print("\n[FULL CONVERSATION HISTORY]")
    print("-" * 60)
    final_history = conv_manager.get_history(session_id)
    for i, msg in enumerate(final_history):
        role = "👤 USER" if msg['role'] == 'user' else "🤖 AI"
        print(f"\n{role}: {msg['content'][:100]}...")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
