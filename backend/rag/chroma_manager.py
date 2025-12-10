import os
from typing import Optional

import dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, SecretStr

dotenv.load_dotenv()

class RAGState(BaseModel):
    question: str
    context: Optional[str] = None
    answer: Optional[str] = None

class ChromaManager:
    def __init__(self, chroma_index_path: str = "data/chroma_db"):
        # --- Step 0: Environment Setup ---
        dotenv.load_dotenv()
        self.chroma_index_path = chroma_index_path
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.environ["AZURE_OPENAI_EMBEDDING_ENDPOINT"],
            api_key=SecretStr(os.environ["AZURE_OPENAI_EMBEDDING_API_KEY"]),
            model="text-embedding-3-small",
            api_version="2024-07-01-preview",
        )
        if os.path.exists(self.chroma_index_path):
            self.vectorstore = Chroma(persist_directory=self.chroma_index_path, embedding_function=self.embeddings)
        else:
            self.vectorstore = Chroma.from_documents([], self.embeddings, persist_directory=self.chroma_index_path)
            self.vectorstore.persist()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 2})
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_LLM_ENDPOINT"],
            api_key=SecretStr(os.environ["AZURE_OPENAI_LLM_API_KEY"]),
            model="GPT-4.1",
            api_version="2024-07-01-preview",
            temperature=0,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a meeting assistant, like a secretary. Use the provided information to answer questions about meetings, agendas, decisions, and participants. Always cite the retrieved info in your answer.",
            ),
            ("human", "{context}\n\nUser question: {question}"),
        ])
        self._build_graph()

    def _build_graph(self):
        def retrieve_node(state: RAGState):
            docs = self.retriever.invoke(state.question)
            context = "\n".join([doc.page_content for doc in docs])
            yield RAGState(question=state.question, context=context, answer=None)

        def generate_node(state: RAGState):
            formatted_prompt = self.prompt.format(
                context=state.context, question=state.question
            )
            answer = self.llm.invoke(formatted_prompt)
            if hasattr(answer, 'content'):
                ans = answer.content
            elif isinstance(answer, list):
                ans = "\n".join(str(a) for a in answer)
            else:
                ans = str(answer)
            yield RAGState(question=state.question, context=state.context, answer=ans)

        builder = StateGraph(RAGState)
        builder.add_node("retrieve", RunnableLambda(retrieve_node))
        builder.add_node("generate", RunnableLambda(generate_node))
        builder.set_entry_point("retrieve")
        builder.add_edge("retrieve", "generate")
        builder.set_finish_point("generate")
        self.rag_graph = builder.compile()

    def store(self, text: str):
        doc = Document(page_content=text)
        self.vectorstore.add_documents([doc])
        self.vectorstore.persist()

    def retrieve(self, question: str) -> str:
        state = RAGState(question=question)
        result = self.rag_graph.invoke(state.model_dump())
        return result["answer"]

# Example usage:
# manager = ChromaManager()
# manager.store("Walmart customers may return electronics within 30 days with a receipt and original packaging.")
# answer = manager.retrieve("What is the return policy for electronics at Walmart?")
# print(answer)
