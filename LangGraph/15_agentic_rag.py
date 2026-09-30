from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    question: str
    context: str
    relevant: bool
    answer: str


documents = [
    "LangGraph is a framework for building stateful AI workflows.",
    "LangGraph uses nodes and edges to define workflows.",
    "LangGraph supports memory through checkpointing.",
    "LangGraph supports human-in-the-loop workflows.",
    "LangGraph can be used to build multi-agent systems.",
]


def retrieve(state: State):
    words = state["question"].lower().split()
    relevant_documents= []

    for doc in documents: 
        for word in words:
            if word in doc.lower():
                relevant_documents.append(doc)
                break

            
    context = "\n".join(relevant_documents)

    print("\nRetriever:")
    print(context)

    return {
        "context": context
    }


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def grade_documents(state: State):
    context = state["context"]

    prompt = f"""
You are grading retrieved documents.

Question:
{state["question"]}

Retrieved documents:
{context}

Are these documents relevant to answering the question?

Reply with ONLY:
YES
or
NO
"""

    response= llm.invoke([
        HumanMessage(content= prompt)
    ])

    result = response.content.strip().upper()

    if "YES" in result:
        return {"relevant": True}

    return {"relevant": False}

def rewrite_question(state: State):
    prompt = f"""
Rewrite the following question so that it is
more useful for retrieving information.

Original question:
{state["question"]}
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "question": response.content
    }

def generate(state: State):

    prompt = f"""
Answer the question using the context below.

Question:
{state["question"]}

Context:
{state["context"]}
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "answer": response.content
    }

def route_after_grading(state: State):

    if state["relevant"]:
        return "generate"

    return "rewrite"


builder = StateGraph(State)

builder.add_node("retrieve", retrieve)
builder.add_node("grade", grade_documents)
builder.add_node("rewrite", rewrite_question)
builder.add_node("generate", generate)

builder.add_edge(START, "retrieve")

builder.add_edge("retrieve", "grade")
builder.add_conditional_edges(
    "grade",
    route_after_grading,
    {
        "generate": "generate",
        "rewrite": "rewrite"
    }
)

builder.add_edge("rewrite", "retrieve")

builder.add_edge("generate", END)

graph = builder.compile()

result = graph.invoke({
    "question": "What is LangGraph?",
    "context": "",
    "relevant": False,
    "answer": ""
})

print("\nFinal answer:")
print(result["answer"])

