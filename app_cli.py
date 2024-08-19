from rag import TestingChat, ChatbotWithSessionHistory
import os
from datetime import datetime

LOG_DIR = "../log/"
if os.path.exists(LOG_DIR) != True:
    os.mkdir(LOG_DIR)

# Generate a unique log file name at the start of the session
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
session_log_file = f'../log/log_response_qwen2_{timestamp}.txt'

def chat():
    chatbot = TestingChat()

    while True:
        question = input("You: ")
        if question.lower() in ["x", "quit"]:
            print("Goodbye!")
            break
        answer = chatbot.ask(question,session_log_file)
        print(f"MCMC Staff: {answer}\n")
        

# def history():
#     chatbot = ChatbotWithSessionHistory()

#     while True:
#         question = input("You: ")
#         if question.lower() in ["x", "quit"]:
#             print("Goodbye!")
#             # chatbot.clear_history()  # Clear history when the session ends
#             break
#         answer = chatbot.ask(question)
#         print(f"Chatbot: {answer}")

if __name__ == "__main__":
    chat()


