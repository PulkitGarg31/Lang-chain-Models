import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

# HuggingFaceEndPoint used for using API of Hugging Face
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="katanemo/Arch-Router-1.5B",
    task = "text-generation"
)
model = ChatHuggingFace(llm = llm)

result = model.invoke("Write a 3 Lines poem on earth.")

print(result.content)