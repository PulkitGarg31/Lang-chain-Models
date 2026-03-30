from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel,Field
from langchain_core.output_parsers import PydanticOutputParser
load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')

class Person(BaseModel):
    name : str = Field(description='Name of the person')
    age : int = Field(description='Age of the person')
    city: str = Field(description='City of the person')
    
parser = PydanticOutputParser(pydantic_object=Person)

 
template1 = PromptTemplate(
    template='Give me the name, age and city of a fictional character \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template1 | model | parser 

result = chain.invoke({'topic' : 'black hole'})

print(result)