import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 1.4)

result = model.invoke("Write a 3 Lines poem on earth.")

print(result)
print("\n")
print(result.content)