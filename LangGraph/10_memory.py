from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    last_message = state["messages"][-1]

    return {
        "messages": [
            AIMessage(
                content=f"You said: {last_message.content}"
            )
        ]
    }

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

result1 = graph.invoke(
    {
        "messages": [
            HumanMessage(content="My name is Attia.")
        ]
    }
, config=config)

result2 = graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is my name?")
        ]
    }
, config=config)

print("First:", result1["messages"][-1].content)
print("Second:", result2["messages"][-1].content)