from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str


def first_node(state: State):
    return {
        "message": state["message"] + " -> First Node"
    }

def second_node(state: State):
    return {
        "message": state["message"] + " -> Second Node"
    }

def third_node(state: State):
    return {
        "message": state["message"] + " -> Third Node"
    }


builder = StateGraph(State)

builder.add_node("first_node", first_node)
builder.add_node("second_node", second_node)    
builder.add_node("third_node", third_node)

builder.add_edge(START, "first_node")
builder.add_edge("first_node", "second_node")
builder.add_edge("second_node", "third_node")
builder.add_edge("third_node", END)

graph = builder.compile()

result = graph.invoke({
    "message": "start"
})

print(result)