from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')
parser = JsonOutputParser()
template1 = PromptTemplate(
    template='Give me the name, age and city of a fictional character \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template1 | model | parser 

result = chain.invoke({})

print(result)