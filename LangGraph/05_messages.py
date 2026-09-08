from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    message: Annotated[list, add_messages]


def first_node(state: State):
    return {
        "message": [
            AIMessage(content="Hello! How can I assist you today?")
        ]
    }


def second_node(state: State):
    return {
        "message": [
            AIMessage(content="Sure! I can help you with that. What specific information are you looking for?")
        ]
    }


builder = StateGraph(State)

builder.add_node("first", first_node)
builder.add_node("second", second_node)
builder.add_edge(START, "first")
builder.add_edge("first", "second") 
builder.add_edge("second", END)

graph = builder.compile()

result = graph.invoke({
    "message": [
        HumanMessage(content="I need help with my account.")
    ]
})

for msg in result["message"]:
    print(f"{type(msg).__name__}: {msg.content}")