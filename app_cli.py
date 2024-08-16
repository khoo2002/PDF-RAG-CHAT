from rag import TestingChat
from langchain_core.messages import HumanMessage, AIMessage


def chat():
    chatbot = TestingChat()

    while True:
        question = input("You: ")
        if question.lower() in ["x", "quit"]:
            print("Goodbye!")
            # chatbot.clear_history()  # Clear history when the session ends
            break
        answer = chatbot.ask(question)
        print(f"Chatbot: {answer}")

if __name__ == "__main__":
    chat()


