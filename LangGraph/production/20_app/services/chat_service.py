from 20_app.graph.chatbot import run_chatbot


def chat(message: str) -> str:
    return run_chatbot(message)