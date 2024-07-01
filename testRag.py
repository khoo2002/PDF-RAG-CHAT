from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings

embedding_model = OllamaEmbeddings(model='nomic-embed-text')
mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
vector_store = mil.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 2, 'lambda_mult': 0.8}
)

mil.max_marginal_relevance_search("What should the terminal equipment be capable of in terms of data message format?")
print(vector_store)
