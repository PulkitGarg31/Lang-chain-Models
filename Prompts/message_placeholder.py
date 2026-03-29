from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chatTemplate = ChatPromptTemplate([
    ('system', 'You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{query}')
])

chat_history = []
with open('Prompts/chat_history.txt') as f:
    chat_history.extend(f.readlines())
    
prompt = chatTemplate.invoke({'chat_history' : chat_history, 'query' : 'Where is my refund'})

print(prompt)
