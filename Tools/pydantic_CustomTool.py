from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a : int = Field(description='First Input variable')
    b : int = Field(description='Second Input variable')
    

def multiply_function(a: int, b: int)->int:
    return a*b

multiply_tool = StructuredTool.from_function(
    func=multiply_function,
    name='multiply',
    description="Multiply two numbers",
    args_schema=MultiplyInput
)

result = multiply_tool.invoke({'a':12, 'b':2})

print(result)

print(multiply_tool.args_schema.model_json_schema())