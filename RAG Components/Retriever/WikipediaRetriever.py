from langchain_community.retrievers import WikipediaRetriever

retriever = WikipediaRetriever(top_k_results=2, lang='en', doc_content_chars_max=1000)

query = "China Russia relations United States geopolitical analysis"

docs = retriever.invoke(query)

for i,doc in enumerate(docs):
    print(f"----Result----{i+1}")
    print(f"Content:\n{doc.page_content}")