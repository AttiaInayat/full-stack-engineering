from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from  operator import add

class State(TypedDict):
    numbers: Annotated[list[int], add]

def first_node(state: State):
    return {
        "numbers": [1,2]
    }

def second_node(state: State):
    return {
        "numbers": [3,4]
    }

builder = StateGraph(State)

builder.add_node("first_node", first_node)
builder.add_node("second_node", second_node)
builder.add_edge(START, "first_node")
builder.add_edge("first_node", "second_node")   
builder.add_edge("second_node", END)

graph = builder.compile()
result = graph.invoke({
    "numbers": []
})

print(result)