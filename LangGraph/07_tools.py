from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def add_numbers(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
llm_with_tools = llm.bind_tools([add_numbers])

def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response]
    }


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()
result = graph.invoke({
    "messages": [
        HumanMessage(content="What is 25 + 17?")
    ]
})

for message in result["messages"]:
    print(type(message).__name__,":" ,message.content)

    if hasattr(message, "tool_calls"):
        print("Tool calls:", message.tool_calls)