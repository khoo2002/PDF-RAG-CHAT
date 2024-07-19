from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.document_loaders import PyPDFDirectoryLoader
import sys
import duckdb
import os
import shutil

PARENT_DATABASE = '../database/' 
DATABASE_PATH = '../database/testing.db'
UPLOAD_FOLDER = '../uploaded'

if os.path.exists(PARENT_DATABASE) != True:
    os.mkdir(PARENT_DATABASE)
    
if os.path.exists(UPLOAD_FOLDER) != True:
    os.mkdir(UPLOAD_FOLDER)

def list_pdf_filenames(path):
    """
    Prints the names of all PDF files in the given directory path.
    """
    # Check if the given path is a directory
    if not os.path.isdir(path):
        print("The provided path is not a valid directory.")
        return

    # List all files in the directory
    files = os.listdir(path)
    
    # Filter and print PDF files
    pdf_files = [file for file in files if file.endswith('.pdf')]
    if pdf_files:
        print("PDF files in the directory:")
        return pdf_files
    else:
        print("No PDF files found in the directory.")

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

    conn = duckdb.connect(DATABASE_PATH)
    result = conn.execute("SELECT * FROM pdf_files").fetchall()
    conn.close()
    print(result)

    if paths == None:
        return True
    for path in paths:
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        mil = Milvus(embedding_function=embedding_model, collection_name='LangChainCollection', drop_old=False, auto_id=True)
        # Assuming PyPDFDirectoryLoader is defined elsewhere and UPLOAD_FOLDER is a constant
        docs = PyPDFDirectoryLoader(path).load()  
        chunks = text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)  # Assuming this function is defined elsewhere
        print(f"Number of chunks: {len(chunks)}")
        mil.add_documents(chunks)
        print("Ingest done for path:", path)
        pdf_files = list_pdf_filenames(path)
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        # Iterate over files in the source directory
        for filename in pdf_files:
            # Check if the current item is a file
            if os.path.isfile(os.path.join(path, filename)):
                try:
                    # Move the file to the destination directory
                    shutil.move(os.path.join(path, filename), os.path.join(UPLOAD_FOLDER, filename))
                    print(f"Moved {filename} to {UPLOAD_FOLDER}")
                except Exception as e:
                    print(f"Failed to move {filename}: {e}")
                    
        for file in pdf_files:
            conn = duckdb.connect(DATABASE_PATH)
            conn.execute("""
            INSERT INTO pdf_files 
            VALUES (nextval('seq_fileid'),'{file_path}', '{file_name}')
            ON CONFLICT (id) DO NOTHING;
            """.format(file_path = os.path.join(UPLOAD_FOLDER,file), file_name = file))
            conn.close()
    
    return True

if __name__ == '__main__':
    paths = sys.argv[1:]  # Get all command line arguments except the script name
    ingest_from_path(paths)
