import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from dotenv import load_dotenv
load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-001', output_dimensionality =8)


documents  = [
    "New Delhi is the capital of India",
    "Kolkata is the capital of West Bengal",
    "Mumbai is the capital of Maharastra",
    "Chennai is the capital of Tamil Nadu"
]

query = "capital of India"

embedded_docs = embedding.embed_documents(documents)
embedded_query = embedding.embed_query(query)

score = cosine_similarity([embedded_query],embedded_docs)[0]

index, score = sorted(list(enumerate(score)), key = lambda x:x[1])[-1]

print(f"Result : {documents[index]}, with Score:{score}")

