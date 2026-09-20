from typing import TypingDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

from dotenv import load_dotenv

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def add_numbers(a:int , b:int) -> int:
    """Add two numbers."""
    return a + b


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
llm_with_tools = llm.bind_tools([add_numbers])

def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response]
    }

def router(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    
    return END


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode([add_numbers]))

builder.add_edge(START, "chatbot")
builder.add_conditional_edge(
    "chatbot",
    router,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge("tools", "chatbot")
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

