from typing import TypedDict 

from langgraph.graph import StateGraph, START, END

class subState(TypedDict):
    message: str


def first_node(state: subState):
    return {
        "message": state["message"] + " -> first node" 
    }

def second_node(state: subState):
    return {
        "message": state["message"] + " -> second node" 
    }

sub_builder = StateGraph(subState)
sub_builder.add_node("first_node", first_node)
sub_builder.add_node("second_node", second_node)
sub_builder.add_edge(START, "first_node")
sub_builder.add_edge("first_node", "second_node")
sub_builder.add_edge("second_node", END)

sub_graph = sub_builder.compile()


class mainState(TypedDict):
    message: str

def start_node(state: mainState):
    return {
        "message": state["message"] + " -> start node" 
    }

def run_subgraph(state: mainState):
    result = sub_graph.invoke({
        "message": state["message"]
    })

    return {
        "message": result["message"]
    }

def end_node(state: mainState):
    return {
        "message": state["message"] + " -> end node" 
    }


builder = StateGraph(mainState)
builder.add_node("start_node", start_node)
builder.add_node("run_subgraph", run_subgraph)
builder.add_node("end_node", end_node)

builder.add_edge(START, "start_node")
builder.add_edge("start_node", "run_subgraph")
builder.add_edge("run_subgraph", "end_node")
builder.add_edge("end_node", END)

main_graph = builder.compile()
result = main_graph.invoke({
    "message": "Initial message"
})

print(result)