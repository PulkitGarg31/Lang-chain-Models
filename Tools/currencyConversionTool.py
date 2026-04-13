from langchain_core.tools import tool, InjectedToolArg
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from typing import Annotated
import requests
import os

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

@tool 
def get_conversion_factor(base_curr: str, target_curr:str) -> float:
    """Get the conversion Rate from base currency to target currency"""
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_curr}/{target_curr}"
    
    response = requests.get(url)
    
    return response.json()['conversion_rate']
@tool
def convert(base_value:int, conversion_factor:Annotated[float,InjectedToolArg]) -> float:
    """This function converts base currency value to target currency value using its conversion rate"""
    return base_value*conversion_factor

model = ChatGoogleGenerativeAI(model = 'gemini-3.1-flash-lite-preview')

llm_with_tools = model.bind_tools([get_conversion_factor,convert])


query = HumanMessage('What is the conversion factor of USD to INR and based on that convert 20 USD to INR')

messages = [query]

ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)
rate = None

for tool_call in ai_message.tool_calls:
    if tool_call['name'] == 'get_conversion_factor':
        rate = get_conversion_factor.invoke(tool_call['args'])
        messages.append(rate)
    elif tool_call['name'] == 'convert':
        result = convert.invoke({
            "base_value": tool_call["args"]["base_value"],
            "conversion_factor": rate
        })
        messages.append(result)
        print(result)
        
print(messages)