from  langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt  = PromptTemplate(
    template= "Generate a 5 line poem on {topic}",
    input_variables=['topic']
)

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite", temperature = 0.8)

chain = prompt | model | parser

result = chain.invoke({'topic': 'Cricket'})

print(result)

# For visulazing the chain we can create a flowchart of it also

chain.get_graph().print_ascii()