import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

from langchain_ollama import ChatOllama

model = ChatOllama(model = "llama3.2")

result = model.invoke("Write a 3 Lines poem on earth.")

print(result.content)

