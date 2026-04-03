# topic -> llm -> report -> llm > summary

from  langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt1  = PromptTemplate(
    template= "Generate a report under 300 words on {topic}",
    input_variables=['topic']
)

prompt2  = PromptTemplate(
    template= "Generate a summary of following text: \n {text}",
    input_variables=['text']
)

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")

chain1 = prompt1 | model | parser

report = chain1.invoke({'topic' : 'cricket'})

print(f"Report:\n{report}")

chain2 = prompt2 | model | parser

summary = chain2.invoke({'text': report})

print(f"Summary:\n{summary}")