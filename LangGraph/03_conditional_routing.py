from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number: int
    result: str


def check_number(state: State):
    print("Checking number.....")
    return {
    }


def even_node(state: State):
    return {
        "result": f"{state['number']} is even"
    }

def odd_node(state: State):
    return {
        "result": f"{state['number']} is odd"
    }


def route_number(state: State):
    if state["number"] % 2 == 0:
        return "even"
    else:
        return "odd"


builder = StateGraph(State)

builder.add_node("even", even_node)
builder.add_node("odd", odd_node)
builder.add_node("check", check_number)

builder.add_edge(START, "check")
builder.add_conditional_edges(
    "check",
    route_number,
    {
        "even": "even",
        "odd": "odd"
    }
)
builder.add_edge("even", END)
builder.add_edge("odd", END)

graph = builder.compile()
result = graph.invoke({
    "number": 12,
    "result": ""
})


print(result)