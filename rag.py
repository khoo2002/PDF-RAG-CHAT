from langchain_community.vectorstores import Milvus
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import os
import sys
from PyPDF2 import PdfMerger

UPLOAD_FOLDER = './uploaded'

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

        singlePdf = pdf_files[0]
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
            singlePdf = pdf_files[0]

        docs = PyPDFLoader(file_path=singlePdf).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        print(f"Number of chunks: {len(chunks)}")

        embedding_model = OllamaEmbeddings(model='jina/jina-embeddings-v2-base-en')
        self.vector_store = Milvus.from_documents(documents=chunks, embedding=embedding_model)

        def relevance_score_fn(score):
            """
            Converts a similarity score to a relevance score with custom logic.
            
            Parameters:
            score (float): The similarity score.

            Returns:
            float: The relevance score.
            """
            # Example: Apply a custom threshold and scaling
            if score > 0.8:
                return 1.0  # Highly relevant
            elif score > 0.5:
                return 0.75  # Moderately relevant
            elif score > 0.3:
                return 0.5  # Less relevant
            else:
                return 0.0  # Not relevant

        self.retriever = self.vector_store.as_retriever(
            # search_type="similarity_score_threshold",
            # search_kwargs={
            #     "k": 5,
            #     "score_threshold": 0.6,
            # },
            # relevance_score_fn=relevance_score_fn,
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
