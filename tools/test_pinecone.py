"""Test PineCone connection and RAG system.

Usage:
    python scripts/test_pinecone.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()


def test_pinecone_connection():
    """Test PineCone API connection."""
    print("=" * 60)
    print("TEST 1: PineCone Connection")
    print("=" * 60)
    
    try:
        from pinecone import Pinecone
        
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            print("❌ PINECONE_API_KEY not found in .env")
            return False
        
        print(f"✅ API Key found: {api_key[:10]}...")
        
        # Initialize client
        pc = Pinecone(api_key=api_key)
        
        # List indexes
        indexes = pc.list_indexes()
        print(f"✅ Connected to PineCone!")
        print(f"📊 Existing indexes: {[idx.name for idx in indexes]}")
        
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_rag_system():
    """Test Advanced RAG system."""
    print("\n" + "=" * 60)
    print("TEST 2: Advanced RAG System")
    print("=" * 60)
    
    try:
        from src.rag.advanced_rag import get_rag_instance
        
        print("Initializing RAG system...")
        rag = get_rag_instance()
        
        # Get stats
        stats = rag.get_stats()
        print("\n📊 RAG System Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ RAG system failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_add_sample_meeting():
    """Test adding a sample meeting."""
    print("\n" + "=" * 60)
    print("TEST 3: Add Sample Meeting")
    print("=" * 60)
    
    try:
        from src.rag.advanced_rag import get_rag_instance
        
        # Force reload to get fresh instance
        rag = get_rag_instance(force_reload=True)
        
        # Sample meeting
        meeting_id = "test_meeting_001"
        transcript = """
        Cuộc họp bắt đầu lúc 9:00 sáng. 
        Chủ đề chính là thảo luận về dự án phát triển ứng dụng AI.
        Nguyễn Văn A trình bày về tiến độ hiện tại.
        Trần Thị B đề xuất sử dụng RAG system với PineCone.
        Quyết định: Sẽ implement RAG system trong tuần tới.
        Action items: 
        - Nguyễn Văn A: Setup PineCone account (deadline: 10/12/2025)
        - Trần Thị B: Research LangChain integration (deadline: 12/12/2025)
        """
        
        metadata = {
            "meeting_type": "meeting",
            "language": "vi",
            "date": "2025-12-06"
        }
        
        print(f"Adding meeting: {meeting_id}")
        success = rag.add_meeting(meeting_id, transcript, metadata)
        
        if success:
            print("✅ Meeting added successfully!")
            
            # Test search
            print("\nTesting search...")
            results = rag.semantic_search("RAG system", k=2)
            print(f"✅ Found {len(results)} results")
            
            if results:
                print("\nFirst result:")
                print(f"  Content: {results[0]['content'][:100]}...")
                print(f"  Metadata: {results[0]['metadata']}")
            
            return True
        else:
            print("❌ Failed to add meeting")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_smart_qa():
    """Test Smart Q&A."""
    print("\n" + "=" * 60)
    print("TEST 4: Smart Q&A")
    print("=" * 60)
    
    try:
        from src.rag.advanced_rag import get_rag_instance
        
        rag = get_rag_instance()
        
        question = "Ai phụ trách setup PineCone?"
        print(f"Question: {question}")
        
        result = rag.smart_qa(question, context_k=2)
        
        print(f"\n✅ Answer: {result['answer']}")
        print(f"\n📚 Sources: {len(result.get('sources', []))} documents")
        
        return True
    except Exception as e:
        print(f"❌ Q&A failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n🚀 Testing PineCone & Advanced RAG System\n")
    
    results = []
    
    # Test 1: Connection
    results.append(("PineCone Connection", test_pinecone_connection()))
    
    # Test 2: RAG System
    results.append(("RAG System Init", test_rag_system()))
    
    # Test 3: Add Meeting
    results.append(("Add Sample Meeting", test_add_sample_meeting()))
    
    # Test 4: Smart Q&A
    results.append(("Smart Q&A", test_smart_qa()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! PineCone RAG system is ready!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
