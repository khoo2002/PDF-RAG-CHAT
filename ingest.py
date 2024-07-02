from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.document_loaders import PyPDFDirectoryLoader
import sys

def ingest_from_path(paths):
    for path in paths:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        mil = Milvus(embedding_function=embedding_model, collection_name='LangChainCollection', drop_old=False)
        # Assuming PyPDFDirectoryLoader is defined elsewhere and UPLOAD_FOLDER is a constant
        docs = PyPDFDirectoryLoader(path).load()  
        chunks = text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)  # Assuming this function is defined elsewhere
        print(f"Number of chunks: {len(chunks)}")
        mil.aadd_documents(chunks)
        print("Ingest done for path:", path)
    return True

if __name__ == '__main__':
    paths = sys.argv[1:]  # Get all command line arguments except the script name
    ingest_from_path(paths)
