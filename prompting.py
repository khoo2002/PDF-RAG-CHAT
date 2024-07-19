import duckdb
from rag import TestingChat
from app import Answer
import datetime
from threading import Thread
import sys
import time


def generate(question, question_id):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    test = TestingChat()
    response_text = test.ask(question)
    print(response_text)
    # Store the answer
    answer_record = {
        'question_id': question_id,  # Use the same question ID as the question
        'answer_text': response_text,
        'created_at': timestamp
    }
    # Measure execution time
    start_time = time.time()

    answer = Answer.store_answer(answer_record)
    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Print the elapsed time
    print(f"Store Answer log - Elapsed time: {elapsed_time} seconds")

    # Measure execution time
    start_time = time.time()

    answer = Answer.get_answer(question_id)
    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Print the elapsed time
    print(f"Verified answer - Elapsed time: {elapsed_time} seconds")

    answer_id = answer['answer'][0]['answer_id']
    print('done')

    return response_text

if __name__ == "__main__":
    print(sys.argv[1])
    print(sys.argv[2] )
    thread = Thread(target = generate, args = (sys.argv[1],sys.argv[2] ))
    thread.start()
    thread.join()
    print("thread finished...exiting")
