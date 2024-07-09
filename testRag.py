from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings
from rag import TestingChat

embedding_model = OllamaEmbeddings(model='nomic-embed-text')
mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
vector_store = mil.as_retriever(
)

mil.similarity_search("What is section 233 in CMA?")
print(vector_store)


test = TestingChat()

for tet in test.askByStream("What is CMA?"):
    print(tet)
    print(type(tet))
