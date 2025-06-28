from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from gmail_integrator import (
    GmailIntegrator,
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


class Agent:
    """
    A simple agent that uses a chat model to respond to user messages.
    It can also respond to emails using the GmailIntegrator."""

    def __init__(
        self, model_name: str, model_provider: str, gmail_integrator: GmailIntegrator
    ):
        self.model = init_chat_model(model_name, model_provider=model_provider)
        self.graph = self.build_graph()
        self.gmail_integrator = gmail_integrator

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

    def run_chatbot(self):
        while True:
            user_input = input("Enter a message: ")
            state = self.graph.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                {"configurable": {"thread_id": "user_thread"}},
            )

            print(f"{state['messages'][-1].content}\n")

    def answer_email(self, sender: str, email_text: str, thread_id: str):
        """
        Answer an email using the chatbot.
        """
        try:
            sender_email = self.parse_sender_email(sender)
            print(f"New email from {sender_email}: \n{email_text}\n")
            state = self.graph.invoke(
                {"messages": [{"role": "user", "content": email_text}]},
                {"configurable": {"thread_id": thread_id}},
            )

            print(f"Chatbot response: {state['messages'][-1].content}\n")

            self.gmail_integrator.reply_to_thread(
                recipient_email=sender_email,
                message_text=state["messages"][-1].content,
                thread_id=thread_id,
            )
        except Exception as e:
            print(f"Error processing email: {e}")

    def parse_sender_email(self, sender_email: str) -> str:
        """
        The sender email is expected to be in the format "Name <email>"
        This function extracts the email part.
        """
        if "<" in sender_email and ">" in sender_email:
            return sender_email.split("<")[1].split(">")[0].strip()
        return sender_email.strip()
