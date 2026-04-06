import os
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')

parser = StrOutputParser()

prompt = PromptTemplate(
    template='Generate a short explanation of {text}',
    input_variables=['text']
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'text.txt')

loader = TextLoader(file_path, encoding= 'utf-8')

docs = loader.load()

chain = prompt | model | parser 

result = chain.invoke({'text':docs[0].page_content})

print(result)