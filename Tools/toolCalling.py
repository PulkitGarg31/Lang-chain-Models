from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()

@tool
def multiply(a: int, b: int)->int:
    """Multiply Two Numbers"""
    return a*b

@tool
def add(a: int, b: int)->int:
    """Add Two Numbers"""
    return a+b

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')

llm_with_tools = llm.bind_tools([add,multiply])

simply_query = llm_with_tools.invoke('Hi')

ToolRequiredQuery = llm_with_tools.invoke('Add 2 and 3')

# Here tool call will be empty
print(simply_query)

#here tool call will be in result
print(ToolRequiredQuery)

# If we send tool call to llm it will return toolmessage
tool_call = ToolRequiredQuery.tool_calls[0]

if tool_call["name"] == "add":
    result = add.invoke(tool_call["args"])
elif tool_call["name"] == "multiply":
    result = multiply.invoke(tool_call["args"])


print(result)
