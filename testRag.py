# from langchain_community.vectorstores import Milvus
# from langchain_community.embeddings import OllamaEmbeddings
from rag import TestingChat

import itertools
import time
from flask import Flask, Response, redirect, request, url_for
import json

app = Flask(__name__)


# embedding_model = OllamaEmbeddings(model='nomic-embed-text')
# mil = Milvus(embedding_function=embedding_model, collection_name = 'LangChainCollection', drop_old = False)
# vector_store = mil.as_retriever(
# )
#embedding_query = embedding_model.embed_query("What is section 233 in CMA?")
#print(mil.similarity_search("What is section 233 in CMA?", k=10))

test = TestingChat()
@app.route('/streamByJson', methods=['POST'])
def prompting():
    if request.method == 'POST':
        json_dict = request.get_json()
        answer = ""
        def generate():
           for i in enumerate(test.askByStream(json_dict['prompt'])):
               json_data = json.dumps({"response": i})
               answer = answer + i
               yield f"data: {json_data}\n\n"
        print(answer)
        return Response(generate(), mimetype='text/event-stream')
    else:
        return "Bad Request", 404
    

if __name__ == "__main__":
    app.run(host='localhost', port=23423)
