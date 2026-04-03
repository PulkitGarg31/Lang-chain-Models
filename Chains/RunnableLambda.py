#                                 --> Runnable Passthrough
# prompt on joke -> llm -> joke -
#                                 --> No. of words in Joke using Runnable Lambda

from  langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')
parser = StrOutputParser()

prompt = PromptTemplate(
    template='Tell me a Joke on {topic}',
    input_variables=['topic']
)

chain = prompt | model | parser |{
    'joke' : RunnablePassthrough(),
    'words' : RunnableLambda(lambda x : len(x.split()))
}

result = chain.invoke({'topic':'war'})

print(result)