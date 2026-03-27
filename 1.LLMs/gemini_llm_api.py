import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
from langchain_google_genai import GoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

model = GoogleGenerativeAI(model = "gemini-3.1-flash-lite-preview")

result = model.invoke("What is highest score in T20i by an individual?")

print(result)