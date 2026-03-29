from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from typing import Literal,Optional

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')

class Review(BaseModel):
    summary: str = Field(description='Generate a summary of the review')
    sentiment: Literal['Positive','Negative','Neutral'] = Field(description='Extract the Sentiment of the review')
    pros: Optional[list[str]] = Field(default=None,description = 'Write all the pros mention in review')
    cons: Optional[list[str]] = Field(default=None,description = 'Write all the cons mention in review')
    
structured_model = model.with_structured_output(Review)

result = structured_model.invoke('The phone has an amazing display and battery life is great, but the camera quality is disappointing and the device heats up sometimes.')

print(result)