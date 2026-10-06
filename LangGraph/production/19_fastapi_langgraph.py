from typing import TypedDict, Annotated

from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    messages : Annotated[list, add_messages]

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.2
)

def chatbot(state: State):
    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }

    
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()


app = FastAPI(
    name="LangGraph Chatbot API",
    description="A simple chatbot API built with LangGraph and FastAPI",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    messages: str

@app.post("/chat")
def chat(request: ChatRequest):

    result = graph.invoke({
        "messages": [
            HumanMessage(content=request.messages)
        ]
    })

    answer = result["messages"][-1].content

    return {
        "answer": answer
    }