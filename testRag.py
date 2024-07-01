from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings

embedding_model = OllamaEmbeddings(model='nomic-embed-text')
vector_store = Milvus(embedding=embedding_model)
print(vector_store)
