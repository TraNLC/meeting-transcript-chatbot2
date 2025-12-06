"""Advanced RAG system with LangChain and multiple vector stores.

Supports:
- ChromaDB (local, free)
- PineCone (cloud, scalable)
- LangChain for advanced chains
- Smart retrieval strategies
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class AdvancedRAG:
    """Advanced RAG system with LangChain integration."""
    
    def __init__(
        self,
        vector_store: str = "chroma",  # "chroma" or "pinecone"
        embedding_model: str = "sentence-transformers",
        llm_provider: str = "gemini"
    ):
        """Initialize Advanced RAG system.
        
        Args:
            vector_store: Vector store to use (chroma or pinecone)
            embedding_model: Embedding model to use
            llm_provider: LLM provider (gemini, openai, etc.)
        """
        print(f"DEBUG: AdvancedRAG init with vector_store='{vector_store}'")
        self.vector_store_type = vector_store
        self.embedding_model_name = embedding_model
        self.llm_provider = llm_provider
        
        # Initialize components
        self._init_embeddings()
        self._init_vector_store()
        self._init_llm()
        
    def _init_embeddings(self):
        """Initialize embedding model."""
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            print("[OK] Embeddings initialized: HuggingFace")
        except ImportError:
            # Fallback to sentence-transformers directly with wrapper
            from sentence_transformers import SentenceTransformer
            from typing import List
            
            class SentenceTransformerEmbeddings:
                def __init__(self, model_name="all-MiniLM-L6-v2"):
                    self.model = SentenceTransformer(model_name)
                
                def embed_documents(self, texts: List[str]) -> List[List[float]]:
                    return self.model.encode(texts).tolist()
                
                def embed_query(self, text: str) -> List[float]:
                    return self.model.encode([text])[0].tolist()
            
            self.embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
            print("[OK] Embeddings initialized: SentenceTransformer (Wrapped)")
    
    def _init_vector_store(self):
        """Initialize vector store (ChromaDB or PineCone)."""
        if self.vector_store_type == "pinecone":
            self._init_pinecone()
        else:
            self._init_chroma()
    
    def _init_chroma(self):
        """Initialize ChromaDB."""
        try:
            from langchain_chroma import Chroma
            
            persist_directory = "data/chroma_langchain"
            os.makedirs(persist_directory, exist_ok=True)
            
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings,
                collection_name="meetings_advanced"
            )
            print("[OK] Vector Store initialized: ChromaDB")
        except Exception as e:
            print(f"[WARN] ChromaDB init failed: {e}")
            self.vector_store = None
    
    def _init_pinecone(self):
        """Initialize PineCone (cloud vector database)."""
        try:
            from langchain_pinecone import PineconeVectorStore
            from pinecone import Pinecone, ServerlessSpec
            
            # Hardcoded for immediate usage as requested
            api_key = "pcsk_5Zg3DW_251rNTDPvMMDQY8RAQXTrZvcaCKZ39rMMzzC5Jwof17xXD2dfAyPqVVFLoJfq9d"
            # api_key = os.getenv("PINECONE_API_KEY", "pcsk_5Zg3DW_251rNTDPvMMDQY8RAQXTrZvcaCKZ39rMMzzC5Jwof17xXD2dfAyPqVVFLoJfq9d")
            index_name = "datacamp-index"
            # index_name = os.getenv("PINECONE_INDEX_NAME", "datacamp-index")
            
            if not api_key:
                print("[WARN] PINECONE_API_KEY not found, falling back to ChromaDB")
                self._init_chroma()
                return
            
            # Initialize Pinecone client (new API)
            pc = Pinecone(api_key=api_key)
            
            # Check if index exists
            # existing_indexes = [index.name for index in pc.list_indexes()]
            
            # if index_name not in existing_indexes:
            #     print(f"Creating PineCone index: {index_name}")
            #     pc.create_index(
            #         name=index_name,
            #         dimension=384,  # all-MiniLM-L6-v2 dimension
            #         metric="cosine",
            #         spec=ServerlessSpec(
            #             cloud="aws",
            #             region="us-east-1"
            #         )
            #     )
            #     print(f"[OK] Index {index_name} created")
            
            # Initialize vector store
            self.vector_store = PineconeVectorStore(
                index_name=index_name,
                embedding=self.embeddings,
                pinecone_api_key=api_key
            )
            print("[OK] Vector Store initialized: PineCone")
        except ImportError as e:
            print(f"[WARN] PineCone library not installed: {e}")
            print("Install with: pip install langchain-pinecone pinecone-client")
            print("Falling back to ChromaDB")
            self._init_chroma()
        except Exception as e:
            print(f"[WARN] PineCone init failed: {e}, falling back to ChromaDB")
            self._init_chroma()
    
    def _init_llm(self):
        """Initialize LLM with LangChain."""
        try:
            if self.llm_provider == "gemini":
                from langchain_google_genai import ChatGoogleGenerativeAI
                
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not found")
                
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    google_api_key=api_key,
                    temperature=0.3,
                    max_tokens=4000
                )
                print("[OK] LLM initialized: Gemini 2.0 Flash")
            else:
                # Fallback to existing LLMManager
                from src.llm import LLMManager
                from src.config import Settings
                
                self.llm_manager = LLMManager(
                    provider="gemini",
                    model_name="gemini-2.5-flash",
                    api_key=Settings.GEMINI_API_KEY
                )
                self.llm = None
                print("[OK] LLM initialized: LLMManager (fallback)")
        except Exception as e:
            print(f"[WARN] LLM init failed: {e}")
            self.llm = None
    
    def add_meeting(
        self,
        meeting_id: str,
        transcript: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Add meeting to vector store.
        
        Args:
            meeting_id: Unique meeting ID
            transcript: Meeting transcript
            metadata: Meeting metadata (type, language, date, etc.)
            
        Returns:
            Success status
        """
        print(f"DEBUG: vector_store = {self.vector_store}")
        print(f"DEBUG: vector_store type = {type(self.vector_store)}")
        
        if self.vector_store is None:
            print("[ERROR] Vector store not initialized")
            return False
        
        try:
            # Split transcript into chunks for better retrieval
            chunks = self._chunk_transcript(transcript)
            
            if not chunks:
                print("[ERROR] No chunks created from transcript")
                return False
            
            # Add metadata to each chunk
            metadatas = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    **metadata,
                    "meeting_id": meeting_id,
                    "chunk_id": i,
                    "timestamp": datetime.now().isoformat()
                }
                metadatas.append(chunk_metadata)
            
            # Add to vector store
            try:
                ids = [f"{meeting_id}_chunk_{i}" for i in range(len(chunks))]
                self.vector_store.add_texts(
                    texts=chunks,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"[OK] Added {len(chunks)} chunks to vector store")
            except AttributeError:
                # Fallback for different vector store APIs
                from langchain_core.documents import Document
                documents = [
                    Document(page_content=chunk, metadata=meta)
                    for chunk, meta in zip(chunks, metadatas)
                ]
                self.vector_store.add_documents(documents, ids=ids)
                print(f"[OK] Added {len(documents)} documents to vector store")
            
            return True
        except Exception as e:
            print(f"[ERROR] Error adding meeting: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _chunk_transcript(self, transcript: str, chunk_size: int = 1000) -> List[str]:
        """Split transcript into chunks.
        
        Args:
            transcript: Full transcript
            chunk_size: Size of each chunk
            
        Returns:
            List of chunks
        """
        # Simple chunking by sentences
        sentences = transcript.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [transcript]
    
    def semantic_search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Semantic search across all meetings.
        
        Args:
            query: Search query
            k: Number of results
            filter_metadata: Filter by metadata (e.g., meeting_type, language)
            
        Returns:
            List of relevant chunks with metadata
        """
        if not self.vector_store:
            print("[ERROR] Vector store not initialized")
            return []
        
        try:
            # Check if there are any documents
            try:
                count = self.vector_store._collection.count()
                if count == 0:
                    print("[WARN] No documents in vector store yet")
                    return []
            except:
                pass
            
            # Perform similarity search
            if filter_metadata:
                results = self.vector_store.similarity_search(
                    query,
                    k=k,
                    filter=filter_metadata
                )
            else:
                results = self.vector_store.similarity_search(query, k=k)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": getattr(doc, 'score', None)
                })
            
            print(f"[OK] Found {len(formatted_results)} results")
            return formatted_results
        except Exception as e:
            print(f"[ERROR] Search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def smart_qa(self, question: str, context_k: int = 3) -> Dict[str, Any]:
        """Smart Q&A with RAG.
        
        Args:
            question: User question
            context_k: Number of context chunks to retrieve
            
        Returns:
            Answer with sources
        """
        if not self.vector_store:
            return {
                "answer": "❌ Vector store chưa được khởi tạo. Vui lòng upload và phân tích một cuộc họp trước.",
                "sources": [],
                "context_used": 0
            }
        
        try:
            # Retrieve relevant context
            relevant_docs = self.semantic_search(question, k=context_k)
            
            if not relevant_docs:
                return {
                    "answer": "Không tìm thấy thông tin liên quan trong các cuộc họp đã lưu.",
                    "sources": []
                }
            
            # Build context
            context = "\n\n".join([doc["content"] for doc in relevant_docs])
            
            # Generate answer using LLM
            if self.llm:
                # Use LangChain LLM
                try:
                    from langchain.prompts import PromptTemplate
                except ImportError:
                    from langchain_core.prompts import PromptTemplate
                
                template = """Dựa trên context sau đây từ các cuộc họp, hãy trả lời câu hỏi một cách chính xác và chi tiết.

Context:
{context}

Câu hỏi: {question}

Trả lời (bằng tiếng Việt):"""
                
                prompt = PromptTemplate(
                    template=template,
                    input_variables=["context", "question"]
                )
                
                formatted_prompt = prompt.format(context=context, question=question)
                response = self.llm.invoke(formatted_prompt)
                answer = response.content if hasattr(response, 'content') else str(response)
            else:
                # Fallback to LLMManager
                prompt = f"""Dựa trên context sau đây từ các cuộc họp, hãy trả lời câu hỏi một cách chính xác và chi tiết.

Context:
{context}

Câu hỏi: {question}

Trả lời (bằng tiếng Việt):"""
                
                answer = self.llm_manager.generate(prompt)
            
            # Extract sources
            sources = [
                {
                    "meeting_id": doc["metadata"].get("meeting_id"),
                    "content_preview": doc["content"][:200] + "...",
                    "metadata": doc["metadata"]
                }
                for doc in relevant_docs
            ]
            
            return {
                "answer": answer,
                "sources": sources,
                "context_used": len(relevant_docs)
            }
        except Exception as e:
            print(f"Q&A error: {e}")
            return {
                "answer": f"Lỗi khi xử lý câu hỏi: {str(e)}",
                "sources": []
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics.
        
        Returns:
            Statistics dictionary
        """
        try:
            count = 0
            type_counts = {}
            language_counts = {}
            
            if self.vector_store:
                if self.vector_store_type == "chroma":
                    try:
                        collection = self.vector_store._collection
                        # Chroma collection.get() returns raw data
                        data = collection.get(include=['metadatas'])
                        count = len(data['ids'])
                        
                        # Aggregation
                        if data['metadatas']:
                            for meta in data['metadatas']:
                                m_type = meta.get('meeting_type', 'unknown')
                                lang = meta.get('language', 'unknown')
                                type_counts[m_type] = type_counts.get(m_type, 0) + 1
                                language_counts[lang] = language_counts.get(lang, 0) + 1
                    except Exception as e:
                        print(f"Stats error: {e}")
                else:
                    # PineCone stats (simplified)
                    count = "N/A"
            
            return {
                "vector_store": self.vector_store_type,
                "total_meetings": count, # Using total_meetings key to match UI
                "total_chunks": count,
                "by_type": type_counts,
                "by_language": language_counts,
                "embedding_model": self.embedding_model_name,
                "llm_provider": self.llm_provider,
                "status": "active" if self.vector_store is not None else "inactive"
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }


# Singleton instance
_rag_instance = None

def get_rag_instance(force_reload: bool = False, vector_store: str = None) -> AdvancedRAG:
    """Get or create RAG instance."""
    global _rag_instance
    if _rag_instance is None or force_reload:
        if vector_store is None:
            vector_store = os.getenv("VECTOR_STORE", "chroma")  # or "pinecone"
        print(f"Creating new RAG instance with vector_store={vector_store}")
        _rag_instance = AdvancedRAG(vector_store=vector_store)
    return _rag_instance
