from langchain_community.vectorstores import Milvus
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import JinaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import os
import sys
from PyPDF2 import PdfMerger

UPLOAD_FOLDER = '/home/khoo/Downloads/llm/llama3/zhaowei_module/uploaded'

class TestingChat:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="llama3")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use one sentences
             minimum and keep the answer concise. The answer must be in the same language that the Question used. 
             Please check carefully and remember to quote all the sources.  [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    def ingest(self):
        self.clear()
        pdf_files = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
        if len(pdf_files) <= 0:
            return
        print(pdf_files)

        singlePdf = os.path.join(UPLOAD_FOLDER, "safesystemMerge.pdf")
        if len(pdf_files) > 1:
            output_dir = singlePdf
            print("merging ...")
            merger = PdfMerger()
            for folder in pdf_files:
                merger.append(open(folder, 'rb'))
            with open(output_dir, "wb") as fout:
                merger.write(fout)
            print("merging done")
        else:
            singlePdf = os.path.join(UPLOAD_FOLDER, pdf_files[0])

        docs = PyPDFLoader(file_path=singlePdf).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        embedding_model = JinaEmbeddings()
        vector_store = Milvus.from_documents(documents=chunks, embedding=embedding_model)
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,
                "score_threshold": 0.6,
            },
        )

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
