from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.document_loaders import PyPDFDirectoryLoader
import sys
import duckdb
import os
import shutil  # Import shutil for file operations

PARENT_DATABASE = '../database/' 
DATABASE_PATH = '../database/testing.db'
UPLOAD_FOLDER = '../uploaded/'


# Ensure the directories exist
if not os.path.exists(PARENT_DATABASE):
    os.mkdir(PARENT_DATABASE)

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

def list_pdf_filenames(path):
    """
    Returns a list of names of all PDF files in the given directory path.
    """
    if not os.path.isdir(path):
        print("The provided path is not a valid directory.")
        return []

    files = os.listdir(path)
    pdf_files = [file for file in files if file.endswith('.pdf')]
    return pdf_files

def ingest_from_path(paths):
    conn = duckdb.connect(DATABASE_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            file_name TEXT
        );
        
        CREATE SEQUENCE IF NOT EXISTS seq_fileid START 1;
    """)
    conn.close()

    for path in paths:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        mil = Milvus(embedding_function=embedding_model, collection_name='LangChainCollection', drop_old=False, auto_id=True)
        
        docs = PyPDFDirectoryLoader(path).load()  
        chunks = text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)  # Assuming this function is defined elsewhere
        print(f"Number of chunks: {len(chunks)}")
        mil.add_documents(chunks)
        print("Ingest done for path:", path)

        pdf_files = list_pdf_filenames(path)
        for file in pdf_files:
            old_path = os.path.join(path, file)
            new_path = os.path.join(UPLOAD_FOLDER, file)

            # Move file to the new location
            shutil.move(old_path, new_path)

            # Update the database with the new path
            conn = duckdb.connect(DATABASE_PATH)
            conn.execute("""
            INSERT INTO pdf_files 
            VALUES (nextval('seq_fileid'),'{file_path}', '{file_name}')
            ON CONFLICT (id) DO NOTHING;
            """.format(file_path=new_path, file_name=file))
            conn.close()

    return True

if __name__ == '__main__':
    paths = sys.argv[1:]  # Get all command line arguments except the script name
    ingest_from_path(paths)
