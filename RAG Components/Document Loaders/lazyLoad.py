# Lazy Load on pdf loader code

import os
from langchain_community.document_loaders import PyPDFLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'test.pdf')

loader = PyPDFLoader(file_path)

docs = loader.lazy_load()

for document in docs:
    print(document.metadata)