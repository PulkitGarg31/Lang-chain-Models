import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'directory')

loader = DirectoryLoader(
    path = file_path,
    glob= '*.txt',
    loader_cls=TextLoader
)

docs = loader.load()

print(docs)