from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

documents = [
    Document(page_content="LangChain makes it easy to work with LLMs."),
    Document(page_content="LangChain is used to build LLM based applications."),
    Document(page_content="Chroma is used to store and search document embeddings."),
    Document(page_content="Embeddings are vector representations of text."),
    Document(page_content="MMR helps you get diverse results when doing similarity search."),
    Document(page_content="LangChain supports Chroma, FAISS, Pinecone, and more."),
]

embedding_model = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-001')

vector_store = Chroma.from_documents(
    documents= documents,
    embedding=embedding_model,
    collection_name="MMR"
)

retriever = vector_store.as_retriever(
    search_type = "mmr",
    search_kwargs = {"k": 3, "lambda_mult":0.5} # relevance-diversity balance lies b/w 0 to 1 if 1 doesn't care if simialr or not
)

query = "What is langchain?"
results = retriever.invoke(query)

for doc in results:
    print(doc.page_content)
    
    