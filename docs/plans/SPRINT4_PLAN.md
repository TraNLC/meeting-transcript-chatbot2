# 🚀 Sprint 4 Plan - RAG with LangChain

**Workshop Date**: Saturday, December 7, 2025  
**Duration**: 1 hour  
**Format**: Virtual via MS Teams  
**Team**: Team 3 - Akatsuki

---

## 📋 Sprint 4 Overview

Apply RAG (Retrieval-Augmented Generation) to Meeting Transcript Chatbot using:
- **Vector Store** (FAISS/Pinecone) for knowledge retrieval
- **LangChain** for RAG pipeline management
- **Function calling** to extend chatbot capabilities

---

## 🎯 Workshop 4 Goals

### Goal
Enhance Meeting Transcript Chatbot with RAG capabilities:
- Store meeting transcripts in vector database
- Retrieve relevant context for questions
- Use LangChain for RAG pipeline
- Add function calling for advanced queries

### Deliverables (1 hour)
1. **Vector store** with meeting transcripts
2. **LangChain RAG chain** for Q&A
3. **Function calling** for specific queries
4. **Enhanced chatbot** with retrieval
5. **Demo** showing RAG benefits

### Schedule (1 hour)
- **0-15 min**: Setup vector store & load transcripts
- **15-30 min**: Build LangChain RAG chain
- **30-45 min**: Add function calling
- **45-60 min**: Test & demo

---

## 📅 Preparation (Dec 1-6)

### Technical Setup
- [ ] Install LangChain: `pip install langchain`
- [ ] Install FAISS: `pip install faiss-cpu`
- [ ] Or Pinecone: `pip install pinecone-client`
- [ ] Review existing chatbot code
- [ ] Prepare sample transcripts

### Knowledge Prep
- [ ] Study LangChain RAG documentation
- [ ] Learn vector store concepts
- [ ] Review function calling patterns
- [ ] Understand retrieval strategies

---

## 💻 Implementation Plan

### 1. Vector Store Setup
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Load meeting transcripts
transcripts = load_all_transcripts()

# Create embeddings
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(transcripts, embeddings)

# Save for reuse
vectorstore.save_local("meeting_transcripts_db")
```

### 2. RAG Chain for Q&A
```python
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load vector store
vectorstore = FAISS.load_local("meeting_transcripts_db", embeddings)

# Create RAG chain
llm = ChatOpenAI(model="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# Query
result = qa_chain({"query": "What were the action items?"})
print(result["result"])
print(result["source_documents"])
```

### 3. Function Calling Integration
```python
from langchain.agents import initialize_agent, Tool

# Define tools
tools = [
    Tool(
        name="SearchTranscripts",
        func=vectorstore.similarity_search,
        description="Search meeting transcripts"
    ),
    Tool(
        name="GetActionItems",
        func=extract_action_items,
        description="Extract action items from transcript"
    )
]

# Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description"
)

# Use agent
agent.run("Find action items for Alice")
```

---

## 👥 Team Roles (5 members)

1. **Khang Vo Duy** - LangChain Integration
   - Setup LangChain RAG chain
   - Integrate with existing LLM code

2. **Hoang Le Viet** - Vector Store Setup
   - Setup FAISS/Pinecone
   - Load & index transcripts

3. **Hoang Pham Minh** - RAG Pipeline
   - Build retrieval logic
   - Optimize search results

4. **Tri Nguyen Quoc** - Function Calling
   - Define function schemas
   - Implement agent tools

5. **Huy Bui Ngoc Phuc** - UI Integration
   - Add RAG features to Gradio
   - Display source documents

**Support**: Dung Nguyen Thi (Testing), Team Lead (Presentation)

---

## 🎯 Enhanced Features

### New Capabilities
1. **Q&A over Multiple Transcripts**
   - Ask questions across all meetings
   - Get relevant context automatically

2. **Source Citation**
   - Show which transcript contains answer
   - Display relevant excerpts

3. **Advanced Queries**
   - "Find all action items for Alice"
   - "What decisions were made about budget?"
   - "Compare topics across meetings"

4. **Better Context**
   - Retrieve relevant meeting sections
   - More accurate responses
   - Less hallucination

---

## ✅ Success Criteria

### Technical
- [ ] Vector store populated with transcripts
- [ ] LangChain RAG chain working
- [ ] Q&A over multiple transcripts
- [ ] Source citation displayed
- [ ] Function calling integrated

### Demo
- [ ] Show RAG vs non-RAG comparison
- [ ] Demonstrate source citation
- [ ] Show advanced queries
- [ ] Clear presentation

---

## 📚 Resources

- LangChain: https://python.langchain.com/
- FAISS: https://faiss.ai/
- Pinecone: https://www.pinecone.io/
- LangGraph: https://langchain-ai.github.io/langgraph/

---

## 📊 Before vs After RAG

| Feature | Sprint 1-3 | Sprint 4 (with RAG) |
|---------|------------|---------------------|
| Q&A | Single transcript | Multiple transcripts |
| Context | Full transcript sent | Relevant chunks only |
| Accuracy | Good | Better (with context) |
| Source | Unknown | Cited with excerpts |
| Queries | Basic | Advanced (function calling) |
| Scalability | Limited | High (vector search) |

---

**Workshop**: Saturday, Dec 7, 2025 | 1 hour | MS Teams  
**Team**: Team 3 - Akatsuki 🔥
