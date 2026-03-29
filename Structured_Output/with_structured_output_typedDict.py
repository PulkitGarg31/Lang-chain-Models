from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated,Literal,Optional

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')

class Review(TypedDict):
    summary: Annotated[str,'Generate a summary of the review']
    sentiment: Annotated[Literal['Positive','Negative','Neutral'],'Extract the Sentiment of the review']
    pros: Annotated[Optional[list[str]],'Write all the pros mention in review']
    cons: Annotated[Optional[list[str]],'Write all the cons mention in review']
    
structured_model = model.with_structured_output(Review)

result = structured_model.invoke('The phone has an amazing display and battery life is great, but the camera quality is disappointing and the device heats up sometimes.')

print(result)