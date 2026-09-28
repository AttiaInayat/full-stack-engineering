from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    message: str


def human_approval(state: State):
    answer = interrupt("Do you approve this action?")

    return {
        "message": f"User response: {answer}"
    }

builder = StateGraph(State)
builder.add_node("human", human_approval)
builder.add_edge(START, "human")
builder.add_edge("human", END)

memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

result1 = graph.invoke(
    {
        "message": "Please approve this action."
    },
    config=config

)

print("Result1: ", result1)

result2 = graph.invoke(
    Command(resume="yes"),
    config=config

)
print("Result2: ", result2["message"])