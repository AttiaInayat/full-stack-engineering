from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from operator import add


class State(TypedDict):
    results: Annotated[list[str], add]


def research(state: State):
    return {
        "results": ["Research completed"]
    }

def analysis(state: State):
    return {
        "results": ["Analysis completed"]
    }

def writing(state: State):
    return {
        "results": ["Writing completed"]
    }

builder = StateGraph(State)
builder.add_node("research", research)
builder.add_node("analysis", analysis)
builder.add_node("writing", writing)

builder.add_edge(START, "research")
builder.add_edge(START, "analysis")
builder.add_edge(START, "writing")

builder.add_edge("research", END)
builder.add_edge("analysis", END)   
builder.add_edge("writing", END)

graph = builder.compile()

result = graph.invoke({
    "results": []
})

print(result)