import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEmbeddings(model_name = "Qwen/Qwen3-Embedding-0.6B", encode_kwargs = {"truncate_dim": 32})

documents  = [
    "New Delhi is the capital of India",
    "Kolkata is the capital of West Bengal",
    "Mumbai is the capital of Maharastra",
    "Chennai is the capital of Tamil Nadu"
]
result_query = embedding.embed_query("New Delhi is the capital of India")
result_docs = embedding.embed_documents(documents)

print(f"For Single strings : {str(result_query)}\nFor Multiple strings:{str(result_docs)}")