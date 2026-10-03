from typing import TypedDict 

from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    question: str
    answer: dict

class PersonInfo(BaseModel):
    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")
    field: str = Field(description="The person's field of expertise")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(PersonInfo)

def extract_info(state: State):
    response = structured_llm.invoke([
        HumanMessage(content=state["question"])
    ])

    return {
        "answer": response.model_dump()
    }


builder = StateGraph(State)
builder.add_node("extract_info", extract_info)
builder.add_edge(START, "extract_info")
builder.add_edge("extract_info", END)

graph = builder.compile()

result = graph.invoke({
    "question": """
    My name is Attia. I am 22 years old and I am
    studying Artificial Intelligence.
    """,
    "answer": {}
})

print("Result\n")
print(result)


print("\nName:", result["answer"]["name"])
print("Age:", result["answer"]["age"])
print("Field:", result["answer"]["field"])