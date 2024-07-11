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
import re
# from documents import Documents
adding_pack = """Section 1, Short title
Section 2, Commencement
Section 3, Objects
Section 4, Territorial and extra-territorial application
Section 5, Power of the Minister to exclude certain persons, geographical areas, etc.
Section 6, Interpretation
Section 7, Direction by the Minister
Section 8, Variation of a direction
Section 9, Register of directions
Section 10, Determination by the Minister
Section 11, Variation of a determination
Section 12, Register of determinations
Section 13, Declaration by the Minister
Section 14, Modification, variation or revocation of a declaration
Section 15, Register of declarations
Section 16, Minister’s power to make regulations
Section 17, Establishment of the Appeal Tribunal
Section 18, Matters which the Appeal Tribunal may review
Section 19, Qualifications of members
Section 20, Resignation and termination of an appointment
Section 21, Vacation of office and acting appointments
Section 22, Quorum for the Appeal Tribunal
Section 23, Decision
Section 23A, Enforcement of decision of Appeal Tribunal
Section 24, Appeal Tribunal procedures
Section 24A, Powers of Appeal Tribunal
Section 25, Suspension of member
Section 26, Disclosure of interest
Section 26A, Secretary of Appeal Tribunal and other officers
Section 26B, Obligation of secrecy
Section 26C, Public servants and public officers
Section 26D, Application of Public Authorities Protection Act 1948
Section 26E, Act or omission done in good faith
Section 27, Application for an individual licence
Section 28, Further information
Section 29, Recommendation by the Commission
Section 30, Grant of an individual licence
Section 31, Restriction on the grant of an individual licence
Section 32, Compliance with the conditions of an individual licence
Section 33, Modification, variation or revocation of individual licence conditions
Section 34, Renewal of an individual licence
Section 35, Surrender of an individual licence
Section 36, Transfer of an individual licence or change of ownership
Section 37, Recommendation for the suspension or cancellation of an individual licence
Section 38, Suspension or cancellation of an individual licence by the Minister
Section 39, Effective date of suspension or cancellation of an individual licence
Section 40, Publication on suspension or cancellation of an individual licence
Section 41, Effect of suspension, cancellation, surrender or expiry of an individual licence
Section 42, Register of individual licences
Section 43, Rights and obligations attached to an individual licence
Section 44, Minister may grant class licence
Section 45, Application for registration
Section 46, Requirement for registration
Section 47, Recommendation by the Commission
Section 48, Cancellation of registration by the Minister
Section 49, Register of class licences
Section 50, Register of registration notices
Section 51, Directions by the Commission
Section 52, Modification, variation or revocation of a direction by the Commission
Section 53, Offence for non-compliance with a direction of the Commission
Section 54, Register of directions
Section 55, Determination by the Commission
Section 56, Modification, variation or revocation of a determination by the Commission
Section 57, Register of determinations
Section 58, Inquiry by the Commission
Section 59, Combining two or more inquiries
Section 60, Conduct of an inquiry
Section 61, Inquiry shall be public
Section 62, Exceptions to a public inquiry
Section 63, Confidential material not to be disclosed
Section 64, Directions about an inquiry
Section 65, Report on an inquiry
Section 66, Protection from civil action
Section 67, Register of reports
Section 68, Investigation by the Commission
Section 69, Complaints to the Commission
Section 70, Conduct of investigation
Section 71, Report on investigation
Section 72, Publication of reports
Section 73, Provision of information
Section 74, Offence for non-compliance
Section 75, Offence for giving false or misleading information, evidence or document, etc.
Section 76, Proof of compliance
Section 77, Commission may retain documents
Section 78, Incorrect record
Section 79, Record of information
Section 80, Publication of information
Section 81, Register of all matters
Section 82, Disputes
Section 83, Notification of a dispute
Section 84, Commission to act only upon notification
Section 85, Commission may publish guidelines
Section 86, Commission to decide notified dispute
Section 87, Decision to be in writing
Section 88, Register of decisions
Section 89, Enforcement
Section 90, Application for the registration of agreements
Section 91, When the Commission shall register the agreement
Section 92, Effect of registration
Section 93, Content of the register of agreements
Section 94, Industry forum
Section 95, Code by the industry forum
Section 96, Commission may determine a voluntary industry code
Section 97, Applicable voluntary industry code
Section 98, Compliance with a registered voluntary industry code a legal defence
Section 99, Directions to comply with a registered voluntary industry code
Section 100, Civil penalty for non-compliance
Section 101, Revocation of a code
Section 102, Submission of new voluntary industry code by an industry forum
Section 103, Register of current voluntary industry code
Section 104, Determination of a mandatory standard
Section 105, Mandatory standard to be consistent
Section 106, Modification, variation or revocation of a mandatory standard
Section 107, Mandatory standard to take precedence
Section 108, Compliance with a mandatory standard a legal defence
Section 109, Civil penalty for non-compliance
Section 110, Undertaking by a person
Section 111, Registration of an undertaking
Section 112, Rules regarding undertakings
Section 113, Withdrawal of an undertaking
Section 114, Replacement of an undertaking
Section 115, Register of undertakings
Section 116, Enforcement of an undertaking
Section 117, Regulatory forbearance
Section 118, Determination by the Minister
Section 119, Review by the Commission
Section 120, Review by the Appeal Tribunal
Section 121, Judicial review
Section 122, Review of subsidiary legislation by the Commission
Section 123, Report to the Minister on industry performance
Section 124, Matters to monitor and report
Section 125, Report to be published
Section 126, Licensing of network facilities, network services and applications services
Section 127, Compliance with licence conditions
Section 128, Definition of network boundary
Section 129, Exemption for applications service provider not subject to a class licence
Section 130, Nominated facilities provider
Section 131, Providers under a class licence shall register
Section 132, Separate licence
Section 133, Prohibition on anticompetitive conduct
Section 134, Commission may publish guidelines
Section 135, Prohibition on entering into collusive agreements
Section 136, Prohibition on tying or linking arrangements
Section 137, Determination of dominant licensee
Section 138, Guidelines as to the meaning of “dominant position”
Section 139, Commission may direct a licensee in a dominant position
Section 140, Authorization of a conduct
Section 141, Register of authorizations
Section 142, Remedies for non-compliance
Section 143, Penalty for offence
Section 144, Minister may make rules
Section 145, Facilities and services which may be included in the access list
Section 146, Determination of facilities and services by the Commission
Section 147, Recommendation by access forum
Section 148, Register of access list
Section 149, Standard access obligations for facilities and services
Section 150, Registration of access agreements
Section 151, Notification of access disputes
Section 152, Access forum
Section 153, Access code
Section 154, Registration of the access code
Section 155, Industry access undertakings
Section 156, Registration of an undertaking
Section 157, Prohibition on using spectrum without assignment
Section 158, Power of the Minister to make regulations
Section 159, Issue of spectrum assignment
Section 160, Spectrum assignment to comply with spectrum plan
Section 161, Reissue of spectrum assignment
Section 162, Third party transfers
Section 163, Transfer rules
Section 164, Issue of apparatus assignment
Section 165, Apparatus assignment to comply with spectrum plan
Section 166, Situation where apparatus assignment shall not be issued
Section 167, Third party authorization
Section 168, Maximum term for an apparatus assignment
Section 169, Class assignment
Section 170, Class assignment to comply with spectrum plan
Section 171, Situation where class assignment shall not be issued
Section 172, Spectrum plan
Section 173, Contents of spectrum plan
Section 174, Preferential rights
Section 175, Dispute about interference
Section 176, Minister may determine spectrum for spectrum assignment
Section 177, Spectrum plan to include procedures for spectrum assignment and apparatus assignment
Section 178, Compulsory acquisition of assignments in determined spectrum
Section 179, Control, planning and administration of numbering and electronic addressing
Section 180, Numbering and electronic addressing plan
Section 181, Management or maintenance of an integrated public number or electronic address database
Section 182, Hindering interoperability an offence
Section 183, Compromising public safety an offence
Section 184, Technical standards forum
Section 185, Matters for technical code
Section 186, Certifying agencies
Section 187, Exemption from offence provisions
Section 188, Provision of network service or applications service
Section 189, Consumer forum
Section 190, Matters for consumer code
Section 191, Publication of consumer code
Section 192, Required applications services
Section 193, Minister’s direction to provide required application service
Section 194, Direction may specify operational details
Section 195, Disputes between consumers and licensees
Section 196, Procedures for consumer complaints
Section 197, Rate setting by providers
Section 198, Principles on rate setting
Section 199, Rate setting by the Minister
Section 200, Power of the Minister to determine persons or areas for special rates
Section 201, Rules regarding rates
Section 202, System of universal service provision
Section 203, Definition of “underserved areas” and “underserved groups within the community”, etc.
Section 204, Universal Service Provision Fund
Section 205, Prohibition on the provision of content applications service
Section 206, Compliance with licence conditions
Section 207, Closed content applications service
Section 208, Exemptions for incidental content
Section 209, Limited content applications service
Section 210, Opinion on category of service
Section 211, Prohibition on provision of offensive content
Section 212, Content forum
Section 213, Content code
Section 214, Inspection of land
Section 215, Installation of network facilities
Section 216, Minimal damage
Section 217, Network facilities provider to restore land
Section 218, Management of activity
Section 219, Agreement with public utility
Section 220, Conditions to which a network facilities installation permit is subject
Section 221, Notice to owner of land
Section 222, Notice to owner of land for lopping of trees, etc.
Section 223, Notice to road authority, public utility, etc.
Section 224, Road, etc., to remain open for passage
Section 225, Network facilities installation permit
Section 226, Criteria for issue of network facilities installation permit
Section 227, Network facilities installation permit has effect subject to this Act and other laws
Section 228, Access to post, network facilities or right-of-way
Section 229, Commission to regulate matters on access to post, etc.
Section 230, Minister may make regulations
Section 231, Offence if use apparatus or device without authority
Section 232, Fraudulent use of network facilities, network services, etc.
Section 233, Improper use of network facilities or network service, etc.
Section 234, Interception and disclosure of communications prohibited
Section 235, Damage to network facilities, etc.
Section 236, Fraud and related activity in connection with access devices, etc.
Section 237, Prohibition on call back service
Section 238, Emission from non-standard equipment or device
Section 239, Unlawful use, possession or supply of non-standard equipment or device
Section 240, Offence for distributing or advertising any communications equipment or device for interception of communication
Section 241, Offence for giving false and misleading statement
Section 242, General offence and penalty
Section 243, Compounding of offences
Section 244, Offences by body corporate
Section 245, Authorized officer
Section 246, Power to investigate
Section 247, Search by warrant
Section 248, Search and seizure without warrant
Section 249, Access to computerized data
Section 250, List of things seized
Section 251, Release of things seized
Section 252, Power to intercept communications
Section 253, Obstruction to search
Section 254, Additional powers
Section 255, Power to require attendance of person acquainted with case
Section 256, Examination of person acquainted with case
Section 257, Admissibility of statements in evidence
Section 258, Authorized officer to complete investigation and hand over to police
Section 259, Prosecution
Section 260, Forfeiture
Section 261, Jurisdiction to try offences
Section 262, Rewards
Section 263, General duty of licensees
Section 264, Persons not liable for act done in good faith
Section 265, Network interception capability
Section 266, Special powers in emergency
Section 267, Disaster plan
Section 268, Minister may make rules on record-keeping
Section 269, Interworking with other authorities
Section 270, Instruments granted under this Act
Section 271, This Act prevails over other Acts
Section 272, Protection of officers and other persons
Section 273, Repeal
Section 274, Dissolution of the Telecommunications Fund
Section 275, Savings
Section 276, Old licences to have effect
Section 277, New class licences to supersede old licences
Section 278, Old licences shall be registered
Section 279, A registered licence shall confer no new benefit
Section 280, Old licensees shall indicate intention
Section 281, Registered licensee may apply for an individual licence under this Act
Section 282, Determination of listed facilities and services
"""

UPLOAD_FOLDER = '../uploaded'

class TestingChat:

    def __init__(self):
        '''
        self.qwen2Model = ChatOllama(model="qwen2:0.5b-instruct-q4_0", temperature=0.4)
        self.gemmaModel = ChatOllama(model="gemma:2b-instruct-q4_0", temperature=0.4)
        self.phi3Model = ChatOllama(model="phi3:3.8b-instruct", top_k=10, top_p=0.5, temperature=0.4, num_predict=80)
        '''
        self.llama3Model = ChatOllama(model="llama3:latest", top_k=10, top_p=0.5, temperature=0.4)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
        '''
        self.qwen2Prompt = PromptTemplate.from_template(
            """
            <|im_start|>system
            You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
            <|im_end|>

            <|im_start|>user
            Question: {question} . **Remember to quote the sources from metadata in Context.**
            Context: {context}
            <|im_end|>
            
            <|im_start|>assistant
            Answer: 
            <|im_end|>
            """
        )
        self.gemmaPrompt = PromptTemplate.from_template(
            """
            <start_of_turn>user
            You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
            Question: {question} . **Remember to quote the sources from metadata in Context.**
            Context: {context}
            <end_of_turn>
            <start_of_turn>model
            """
        )
        self.phi3Prompt = """
        <|system|>
       You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
        **Question**: {question}
        
        **Context**: {option1}. {option2}. {context}
        <|end|>
        
        <|senior staff|>
        **Answer**:
        [Choose the better option based on the context. If needed, restructure the original answers based on the given context. If necessary, provide a new answer based on the question and context]
        **Document Name**: [Insert Document Name]
        """
        '''
        
        self.llama3Prompt = PromptTemplate.from_template("""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
        **Context**: {context} {adding_pack}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.<|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        **Question**: {question} <|eot_id|>
        <|start_header_id|>senior staff<|end_header_id|>
        **Answer**:
        
        **Document Name**: [Insert Document Name]
        """.format(context="{context}",adding_pack=adding_pack,question="{question}"))
        
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
        self.vector_store = mil
        self.retriever = self.vector_store.as_retriever()
        self.initialize_chain()

        # self.docs = Documents()
    def initialize_chain(self):
        print('initialize')
        self.llama3Chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                            | self.llama3Prompt
                            | self.llama3Model
                            | StrOutputParser())
        '''
        self.qwen2Chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                  | self.qwen2Prompt
                  | self.qwen2Model
                  | StrOutputParser())
        
        self.gemmaChain = ({"context": self.retriever, "question": RunnablePassthrough()}
                  | self.gemmaPrompt
                  | self.gemmaModel
                  | StrOutputParser())
        '''
        

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
        
    #LLAMA3
    # def ask(self, query: str):
    #     self.llama3Model = ChatOllama(model="llama3:latest", top_k=10, top_p=0.5, temperature=0.4)
    #     self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)  
    #     self.llama3Prompt = None
    #     if re.search("section", query.lower()) or re.search("cma", query.lower()) or re.search("communications and multimedia act", query.lower()):
    #         self.llama3Prompt = PromptTemplate.from_template("""
    #         <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    #         You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
    #         **Context**: {context} {adding_pack}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.<|eot_id|>
    #         <|start_header_id|>user<|end_header_id|>
    #         **Question**: {question} <|eot_id|>
    #         <|start_header_id|>senior staff<|end_header_id|>
    #         **Answer**:
            
    #         **Document Name**: [Insert Document Name]
    #         """.format(context="{context}",adding_pack=adding_pack,question="{question}"))
    #     else:
    #         self.llama3Prompt = PromptTemplate.from_template("""
    #     <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    #     You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
    #     **Context**: {context}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.<|eot_id|>
    #     <|start_header_id|>user<|end_header_id|>
    #     **Question**: {question} <|eot_id|>
    #     <|start_header_id|>senior staff<|end_header_id|>
    #     **Answer**:
        
    #     **Document Name**: [Insert Document Name]
    #     """)    
        
    #     embedding_model = OllamaEmbeddings(model='nomic-embed-text')
    #     mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
    #     self.vector_store = mil
    #     self.retriever = self.vector_store.as_retriever()
    #     self.llama3Chain = ({"context": self.retriever, "question": RunnablePassthrough()}
    #                         | self.llama3Prompt
    #                         | self.llama3Model
    #                         | StrOutputParser())
    #     return self.llama3Chain.invoke(query)

    # #PHI3
    # def ask(self, query: str):
    #     self.phi3Model = ChatOllama(model="phi3:3.8b-instruct", top_k=10, top_p=0.5, temperature=0.4)
    #     self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)  
    #     self.phi3Prompt = None
    #     if re.search("section", query.lower()) or re.search("cma", query.lower()) or re.search("communications and multimedia act", query.lower()):
    #         self.phi3Prompt = PromptTemplate.from_template("""
    #         <|system|>
    #         You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
    #         **Context**: {context} {adding_pack}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.
    #         <|end|>
    #         <|user|>
    #         **Question**: {question}
    #         <|end|>
    #         <|senior staff|>
    #         **Answer**:
    #         [Give your answer here]
    #         **Document Name**: [Insert Document Name]
    #         """.format(context="{context}",adding_pack=adding_pack,question="{question}"))
    #     else:
    #         self.phi3Prompt = PromptTemplate.from_template("""
    #         <|system|>
    #         You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
    #         **Context**: {context}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.
    #         <|end|>
    #         <|user|>
    #         **Question**: {question}
    #         <|end|>
    #         <|senior staff|>
    #         **Answer**:
    #         [Give your answer here]
    #         **Document Name**: [Insert Document Name]
    #     """)    
        
    #     embedding_model = OllamaEmbeddings(model='nomic-embed-text')
    #     mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
    #     self.vector_store = mil
    #     self.retriever = self.vector_store.as_retriever()
    #     self.phi3Chain = ({"context": self.retriever, "question": RunnablePassthrough()}
    #                         | self.phi3Prompt
    #                         | self.phi3Model
    #                         | StrOutputParser())
    #     return self.phi3Chain.invoke(query)

    #qwen2Model
    def ask(self, query: str):
        self.qwen2Model = ChatOllama(model="qwen2:0.5b-instruct-q4_0", top_k=10, top_p=0.5, temperature=0.4)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)  
        self.qwen2Model = None
        if re.search("section", query.lower()) or re.search("cma", query.lower()) or re.search("communications and multimedia act", query.lower()):
            self.qwen2Prompt = PromptTemplate.from_template("""
            <|im_start|>system
            You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.            
            <|im_end|>
            <|im_start|>user
            Question: {question} . **Remember to quote the sources from metadata in Context.**
            **Context**: {context} {adding_pack}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.
            <|im_end|>
            <|im_start|>assistant
            Answer: 
            **Document Name**: [Insert Document Name]
            <|im_end|>
            """.format(context="{context}",adding_pack=adding_pack,question="{question}"))
        else:
            self.qwen2Prompt = PromptTemplate.from_template("""
            <|im_start|>system
            You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.            
            <|im_end|>
            <|im_start|>user
            Question: {question} . **Remember to quote the sources from metadata in Context.**
            **Context**: {context}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.
            <|im_end|>
            <|im_start|>assistant
            Answer: 
            **Document Name**: [Insert Document Name]
            <|im_end|>
        """)    
        
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
        self.vector_store = mil
        self.retriever = self.vector_store.as_retriever()
        self.qwen2Chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                            | self.qwen2Prompt
                            | self.qwen2Model
                            | StrOutputParser())
        return self.qwen2Chain.invoke(query)


    def askByStream(self, query: str):
        self.llama3Model = ChatOllama(model="llama3:latest", top_k=10, top_p=0.5, temperature=0.4)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)  
        self.llama3Prompt = None
        if re.search("section", query.lower()) or re.search("cma", query.lower()) or re.search("communications and multimedia act", query.lower()):
            self.llama3Prompt = PromptTemplate.from_template("""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
            **Context**: {context} {adding_pack}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.<|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            **Question**: {question} <|eot_id|>
            <|start_header_id|>senior staff<|end_header_id|>
            **Answer**:
            
            **Document Name**: [Insert Document Name]
            """.format(context="{context}",adding_pack=adding_pack,question="{question}"))
        else:
            self.llama3Prompt = PromptTemplate.from_template("""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a senior staff member at the **Malaysian Communications & Multimedia Commission (MCMC)** in **Malaysia**, tasked with fact-checking and answering queries across all relevant topics. Based on the provided context, provide a **concise answer maximum is three sentences** in the same language as the question. If unsure, state that you do not know. Ensure all sources are accurately referenced. **Must add the document name when using**.
        **Context**: {context}. The current Prime Minister is Dato' Sri Anwar Ibrahim from 24 November 2022 until now.<|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        **Question**: {question} <|eot_id|>
        <|start_header_id|>senior staff<|end_header_id|>
        **Answer**:
        
        **Document Name**: [Insert Document Name]
        """)    
        
        embedding_model = OllamaEmbeddings(model='nomic-embed-text')
        mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
        self.vector_store = mil
        self.retriever = self.vector_store.as_retriever()
        self.llama3Chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                            | self.llama3Prompt
                            | self.llama3Model
                            | StrOutputParser())
        return self.llama3Chain.stream(query)
