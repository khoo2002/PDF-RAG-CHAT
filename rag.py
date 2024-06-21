from langchain_community.vectorstores import Milvus
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from fastembed import LateInteractionTextEmbedding
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import os
import sys
from PyPDF2 import PdfMerger

UPLOAD_FOLDER = '../uploaded'

import os

class Documents:
    def __init__(self):
        self.docs = []

    def add(self, doc_path, ingest_status=True):
        # Check if the document already exists with the same path and filename
        if not self._exists(doc_path):
            self.docs.append({doc_path: {"ingest": ingest_status}})
        else:
            print(f"Document '{doc_path}' already exists. Ignoring.")

    def _exists(self, doc_path):
        # Extract filename from doc_path
        filename = os.path.basename(doc_path)
        # Check if any document in self.docs has the same filename
        for doc in self.docs:
            existing_path = list(doc.keys())[0]
            existing_filename = os.path.basename(existing_path)
            if existing_filename == filename:
                return True
        return False

    def clear(self):
        self.docs = []

    def __len__(self):
        return len(self.docs)

    def __getitem__(self, item):
        return self.docs[item]

    def __iter__(self):
        return iter(self.docs)

    def __str__(self):
        return str(self.docs)

    def __repr__(self):
        return repr(self.docs)

    def update_ingest_status(self, doc_path, ingest_status):
        for doc in self.docs:
            if doc_path in doc:
                doc[doc_path]["ingest"] = ingest_status
                break

    def get_all_uningested_files(self):
        return [list(doc.keys())[0] for doc in self.docs if not list(doc.values())[0]["ingest"]]

class TestingChat:
    vector_store = None
    retriever = None
    chain = None
    docs = None

    def __init__(self):
        self.model = ChatOllama(model="qwen2:0.5b")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            [INST] You are a senior staff member at the Malaysian Communications & Multimedia Commission, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. [/INST]
            [INST] Question: {question}
            Context: {context}
            Answer: [/INST]

            """
        )
        self.docs = Documents()

    def ingest(self):
        
        pdf_files = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
        if len(pdf_files) <= 0:
            return
        if len(pdf_files) > 1:
            for folder in pdf_files:
                self.docs.add(folder, ingest_status=False)
            print("adding document done")
        else:
            self.docs.add(pdf_files[0], ingest_status=False)

        docs = PyPDFDirectoryLoader(UPLOAD_FOLDER).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        print(f"Number of chunks: {len(chunks)}")
        
        embedding_model = OllamaEmbeddings(model='jina/jina-embeddings-v2-base-en')
        
        self.vector_store = Milvus.from_documents(documents=chunks, embedding=embedding_model)
        self.retriever = self.vector_store.as_retriever()
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())
        
        print("digest done!")
        if len(pdf_files) <= 0:
            return
        if len(pdf_files) > 1:
            for folder in pdf_files:
                self.docs.update_ingest_status(folder, ingest_status=True)
            print("adding document done")
        else:
            self.docs.update_ingest_status(pdf_files[0], ingest_status=True)
        

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
