from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    task: str
    message: str


def writer(state: State):
    return {
        "message": "Writing completed"
    }

def researcher(state: State):
    return {
        "message": "Research completed"
    }

def supervisor(state: State):
    print("Supervisor reviewing the work...")

    return {}

def router(state: State):
    task = state["task"].lower()

    if "write" in task:
        return "writer"


    if "research" in task:
        return "researcher"

    return END



builder = StateGraph(State)
builder.add_node("writer", writer)
builder.add_node("researcher",researcher)
builder.add_node("supervisor",supervisor)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor",
    router,
    {
        "writer":"writer",
        "researcher":"researcher",
        END: END
    }
)

builder.add_edge("writer",END)
builder.add_edge("researcher",END)

graph= builder.compile()
result= graph.invoke({
    "task": "write about AI.",
    "message":""
})

print("\nResult")
print(result)
    


        