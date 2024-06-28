from langchain_community.vectorstores import Milvus
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import os
import sys
from PyPDF2 import PdfMerger
# from documents import Documents

UPLOAD_FOLDER = '../uploaded'

class TestingChat:

    def __init__(self):
        self.model = None
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
        self.prompt = PromptTemplate.from_template(
            """
            <|im_start|>system
            You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
            <|im_end|>

            <|im_start|>user
            Question: {question}
            Context: {context}
            <|im_end|>
            
            <|im_start|>assistant
            Answer: 
            <|im_end|>
            """
        )
        # self.docs = Documents()
    def initialize_chain(self, model_name="tinydolphin:latest", prompt=""):
        self.model = ChatOllama(model=model_name)
        
        if "" != prompt:
            prompt = PromptTemplate.from_template(prompt)
        self.prompt = prompt
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                  | prompt
                  | self.model
                  | StrOutputParser())

    def ingest(self):        
        # pdf_files = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
        # if len(pdf_files) <= 0:
        #     return
        # if len(pdf_files) > 1:
        #     for folder in pdf_files:
        #         self.docs.add(folder, ingest_status=False)
        #     print("adding document done")
        # else:
        #     self.docs.add(pdf_files[0], ingest_status=False)

        docs = PyPDFDirectoryLoader(UPLOAD_FOLDER).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        print(f"Number of chunks: {len(chunks)}")
        
        # model_name = "BAAI/bge-m3"
        # model_kwargs = {"device": "cpu"}
        # encode_kwargs = {"normalize_embeddings": True}
        # embedding_model = HuggingFaceBgeEmbeddings(
        #     model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
        # )
        
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        
        self.vector_store = Milvus.from_documents(documents=chunks, embedding=embedding_model)
        self.retriever = self.vector_store.as_retriever()
        print("digest done!")
        self.initialize_chain()
        # if len(pdf_files) <= 0:
        #     return
        # if len(pdf_files) > 1:
        #     for folder in pdf_files:
        #         self.docs.update_ingest_status(folder, ingest_status=True)
        #     print("adding document done")
        # else:
        #     self.docs.update_ingest_status(pdf_files[0], ingest_status=True)

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
