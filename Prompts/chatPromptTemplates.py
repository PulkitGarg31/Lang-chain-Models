from langchain_core.prompts import ChatPromptTemplate

chatTemplate = ChatPromptTemplate([
    ('system' , 'You are helpful {domain} expert'),
    ('human' ,'Explain in simple terms, what is {topic}')
])
prompt = chatTemplate.invoke({'domain':'cricket', 'topic' : 'Swing'})
print(prompt)