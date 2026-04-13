from langchain_core.tools import tool

@tool
def multiply(a: int, b: int)->int:
    """Multiply Two Numbers"""
    return a*b

result = multiply.invoke({'a':3, 'b':6})

print(result)

# Atributes of a tool
print(multiply.name)
print(multiply.description)
print(multiply.args)

# This is what llm will see when you send tool to it
print(multiply.args_schema.model_json_schema())