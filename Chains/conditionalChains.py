#                                                               (Pos) --> llm -> Response for Positive
# Product -> llm -> Fake Review - llm -> Sentiment Extraction -
#                                                               (Neg) --> llm -> Response for negative

# topic -> llm -> report -> llm > summary

from  langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch,RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")
parser = StrOutputParser()

review_prompt  = PromptTemplate(
    template= "Generate a review by a customer of {Product} under 80 words",
    input_variables=['Product']
)

senitment_prompt  = PromptTemplate(
    template= "Extract the sentiment of the following review: \n {text}\n {format_instructions}",
    input_variables=['text'],
    partial_variables={'format_instructions': "Reply with only one word: 'pos' or 'neg'"}
)

prompt_pos  = PromptTemplate(
    template= "Being a representative of {Product},Generate a reply from company of {Product} for a positive review: {Review}",
    input_variables=['Product','Review']
)

prompt_neg  = PromptTemplate(
    template= "Being a representative of {Product},Generate a reply from company of {Product} for a negative review: {Review}",
    input_variables=['Product','Review']
)
review_chain = review_prompt | model | parser
sentiment_chain = senitment_prompt | model | parser

def extract_sentiment(inputs: dict) -> dict:
    review = review_chain.invoke(inputs)
    sentiment = sentiment_chain.invoke(review)
    return {
        'Sentiment' : sentiment,
        'Product' : inputs['Product'],
        'Review' : review
    }

branch = RunnableBranch(
    (lambda x: x['Sentiment'] == 'pos', prompt_pos | model | parser),
    (lambda x: x['Sentiment'] == 'pos', prompt_neg | model | parser),
    RunnableLambda(lambda x:f"Unknown sentiment: {x['sentiment']}")
)

final_chain = RunnableLambda(extract_sentiment) | branch

result = final_chain.invoke({'Product':'Samsung S25'})

print(result)