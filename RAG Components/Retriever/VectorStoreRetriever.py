from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()

documents = [
    Document(page_content="LangChain is a framework for building LLM-powered applications.",
             metadata={"source": "doc1", "topic": "langchain"}),

    Document(page_content="ChromaDB is an open-source vector database optimized for AI applications.",
             metadata={"source": "doc2", "topic": "chromadb"}),

    Document(page_content="Gemini is Google's multimodal AI model capable of understanding text, images, and audio.",
             metadata={"source": "doc3", "topic": "gemini"}),

    Document(page_content="Retrieval-Augmented Generation (RAG) combines search with language model generation.",
             metadata={"source": "doc4", "topic": "rag"}),

    Document(page_content="Embeddings are numerical vector representations of text used for semantic similarity search.",
             metadata={"source": "doc5", "topic": "embeddings"}),

    Document(page_content="Vector stores index high-dimensional embeddings and allow fast approximate nearest neighbor search.",
             metadata={"source": "doc6", "topic": "vector-store"}),
]

embedding_model = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-001')

vector_store = Chroma.from_documents(
    documents= documents,
    embedding=embedding_model,
    collection_name="Retriever"
)

retriever = vector_store.as_retriever(search_kwargs = {'k':2})

query = "What is Chromadb?"
result = retriever.invoke(query)

for doc in result:
    print(doc.page_content)
    
    