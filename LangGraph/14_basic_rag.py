from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    context: str


documents = [
    "LangGraph is a framework for building stateful, multi-step AI applications.",
    "LangGraph allows developers to create workflows using nodes and edges.",
    "LangGraph supports memory, human-in-the-loop, tools, and multi-agent systems.",
    "RAG stands for Retrieval-Augmented Generation.",
]

def retreive(state: State):

    question = state["messages"][-1].content.lower()

    relevant_documents = []

    for document in documents:
        words = question.split()

        for word in words:
            if word in document.lower():
                relevant_documents.append(document)
                break

        
    context = "\n".join(relevant_documents)

    return {
        "context": context
    }


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def generate(state: State):

    question = state["messages"][-1].content

    prompt = f"""
Answer the user's question using the context below.

Context:
{state["context"]}

Question:
{question}
"""

    response = llm.invoke([
        HumanMessage(content= prompt)
    ])

    return {
        "messages": [AIMessage(content=response.content)]
    }


builder = StateGraph(State)

builder.add_node("retrieve", retreive)
builder.add_node("generate", generate)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()


result = graph.invoke({
    "messages": [
        HumanMessage(
            content="What is LangGraph?"
        )
    ],
    "context": ""
})


print("Answer:")
print(result["messages"][-1].content)
