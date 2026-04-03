#                         --> llm -> notes -> output
# topic -> llm -> report -
#                         --> llm -> quiz -> output

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
    template= "Generate a notes of following text: \n {text}",
    input_variables=['text']
)

prompt3  = PromptTemplate(
    template= "Generate a quiz from following text: \n {text}",
    input_variables=['text']
)

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")

chain1 = prompt1 | model | parser

chain2 = {
    'notes' : prompt2 | model | parser,
    'quiz' : prompt3 | model | parser
}

final_Chain = chain1 | (lambda x: {'text': x}) |chain2

result = final_Chain.invoke({'topic':'Cricket'})

print(f"Notes:\n{result['notes']}")
print(f"Quiz:\n{result['quiz']}")