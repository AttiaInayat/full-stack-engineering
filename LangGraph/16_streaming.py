from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()


class State(TypedDict):
    messages : Annotated[list, add_messages]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def chatbot(state: State):
    result = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [result]
    }


builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()

input_state = {
    "messages": [
        HumanMessage(content = 
        "Explain artificial intelligence in a simple way."
        )
    ]
}

print("Streaming started...\n")

for chunk in graph.stream(input_state, stream_mode = "updates"):
    print(chunk)

print("\nStreaming finished.")
