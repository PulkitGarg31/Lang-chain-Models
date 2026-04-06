import os
from langchain_community.document_loaders import CSVLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'data.csv')

loader = CSVLoader(file_path)

docs = loader.load()

print(len(docs))
print(docs[0])