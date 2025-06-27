from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

load_dotenv()
model = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}


def main():
    graph_builder = StateGraph(State)

    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile()

    user_input = input("Enter a message: ")
    state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})

    print(state["messages"][-1].content)


if __name__ == "__main__":
    main()
