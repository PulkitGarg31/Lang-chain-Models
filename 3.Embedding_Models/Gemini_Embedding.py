import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-001', output_dimensionality =8)


documents  = [
    "New Delhi is the capital of India",
    "Kolkata is the capital of West Bengal",
    "Mumbai is the capital of Maharastra",
    "Chennai is the capital of Tamil Nadu"
]
result_query = embedding.embed_query("New Delhi is the capital of India")
result_docs = embedding.embed_documents(documents)

print(f"For Single strings : {str(result_query)}\nFor Multiple strings:{str(result_docs)}")
