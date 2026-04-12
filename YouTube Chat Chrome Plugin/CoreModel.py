"""
    We will Create a Youtube Chat Model 
    - Main task - You can chat about the video along with watching it
    Process - Load the transcript of Youtube Video
    Split Text using text splitter and create chunks using it
    Create embedding of them and store it in a vector database
    
    After We get a query we will create its embedding also
    
    and Retrive the realted section chunks from the database

    send this query and our chunks to model with prompt to llms
    
    this we will give a desired results to us.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from cache_manager import cleanup_cache
import os
import re

load_dotenv()

def extract_video_id(url : str) -> str:
    """Extract video id from video url"""
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    
    if not match:
        raise ValueError("Invalid Youtube URL")
    return match.group(1)

def load_transcript(video_id : str) -> str:
    """Fetch and join transcript into a single string."""
    transcript = YouTubeTranscriptApi().fetch(video_id)
    return " ".join(chunk.text for chunk in transcript)

def build_vectorstore(text: str, video_id: str) -> Chroma:
    """Split text into chunks and store embeddings in FAISS."""
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    persist_dir = os.path.join(BASE_DIR, "chroma_db", video_id)
    
    embeddings = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')
    
    if os.path.exists(persist_dir):
        print("Loading cached vectorstore...")
        return Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = splitter.create_documents([text])
    
    return Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)

def get_dynamic_k(text: str) -> int:
    """Auto-adjust k based on transcript length."""
    total_chunks = len(text) // 1000  # approximate number of chunks
    
    if total_chunks <= 10:      # short video (<10 min)
        return 3
    elif total_chunks <= 30:    # medium video (10-30 min)
        return 6
    elif total_chunks <= 60:    # long video (30-60 min)
        return 10
    else:                       # podcast / very long (60min+)
        return 15
    
def build_qa_chain(vectorstore: Chroma, text: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": get_dynamic_k(text)})
    model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash', temperature = 0)
    prompt = PromptTemplate(template = """
                                        You are a helpful assistant answering questions about a YouTube video.
                                        Use the transcript excerpts below to answer as completely as possible.
                                        If asked for a list, extract as many relevant points as you can find across all excerpts.
                                        Only say information is missing if it is truly absent from ALL excerpts.
                                        Transcript excerpts:{context}
                                        Question: {question}
                                        Answer:"""
                            )
    chain = (
        {'context': retriever, 'question':RunnablePassthrough()} |
        prompt | model | StrOutputParser()
    )
    
    return chain


def main():
    cleanup_cache()
    url = input("Enter YouTube video URL: ").strip()
    video_id = extract_video_id(url)
    
    print("Loading transcript...")
    text = load_transcript(video_id)
    
    print("Building vector store...")
    vectorstore = build_vectorstore(text, video_id)
    qa_chain = build_qa_chain(vectorstore,text)
    
    print("\nReady! Ask anything about the video. Type 'quit' to exit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in ("quit", "exit"):
            break
        print("\nAssistant: ", end="", flush=True)
        for chunk in qa_chain.stream(query):
            print(chunk, end="", flush=True)
        print("\n")
        
if __name__ == "__main__":
    main()
