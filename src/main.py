from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
import os
from gmail_integrator import (
    GmailIntegrator,
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


class Agent:
    def __init__(self, model_name: str, model_provider: str):
        self.model = init_chat_model(model_name, model_provider=model_provider)
        self.graph = self.build_graph()
        # Initialize Gmail integration
        self.gmail = GmailIntegrator(
            integration_id=os.getenv("GMAIL_INTEGRATION_ID"), user_id="cli_user"
        )

    def build_graph(self) -> StateGraph:
        """
        Compile the state graph for the agent.
        """
        graph_builder = StateGraph(State)

        # Build simple graph with a single node for the chatbot
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        # Use short-term memory to save the state of the graph (non-persistent)
        checkpointer = InMemorySaver()
        graph = graph_builder.compile(checkpointer=checkpointer)
        return graph

    def chatbot(self, state: State):
        """
        Chatbot function to process user messages.
        """
        return {"messages": [self.model.invoke(state["messages"])]}

    def run(self):
        while True:
            user_input = input("Enter a message: ")
            state = self.graph.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                {"configurable": {"thread_id": "user_thread"}},
            )

            print(f"{state['messages'][-1].content}\n")


def main():
    load_dotenv()

    model_name = "claude-3-5-sonnet-latest"
    model_provider = "anthropic"
    agent = Agent(model_name, model_provider)
    agent.run()


if __name__ == "__main__":
    main()
