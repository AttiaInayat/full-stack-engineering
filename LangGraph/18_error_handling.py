from typing import TypedDict

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number: int
    result: str
    error: str


def divide(state: State):
    try:
        result = 100 / state["number"]
        return {
            "result" : f"Result of division: {result}",
            "error" : ""
        }
    except ZeroDivisionError:
        return {
            "result" : "",
            "error" : "Error: Division by zero is not allowed."
        }

def check_result(state: State):
    if state["error"]:
        print("An error occurred during division:", state["error"])
        return {
        }
    else:
        print("Division successful:", state["result"])
        return {
        }

builder = StateGraph(State)
builder.add_node("divide", divide)
builder.add_node("check_result", check_result)
builder.add_edge(START, "divide")
builder.add_edge("divide", "check_result")
builder.add_edge("check_result", END)

graph = builder.compile()


result = graph.invoke({
    "number": 0,
    "result": "",
    "error": ""
})

print("\nFinal state:")
print(result)