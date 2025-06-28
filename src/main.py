from dotenv import load_dotenv
from gmail_integrator import GmailIntegrator
from agent import Agent
from email_listener import EmailListener
import os
import threading

MODEL_NAME = "claude-3-5-sonnet-latest"
MODEL_PROVIDER = "anthropic"


def run_email_listener(listener: EmailListener):
    """Thread function to run the email listener."""
    listener.start()


def run_chatbot(agent: Agent):
    """Thread function to run the chatbot interface."""
    agent.run_chatbot()


def main():
    load_dotenv()

    gmail_integrator = GmailIntegrator(
        integration_id=os.getenv("GMAIL_INTEGRATION_ID"), user_id="cli_user"
    )

    agent = Agent(MODEL_NAME, MODEL_PROVIDER, gmail_integrator)
    email_listener = EmailListener(gmail_integrator, agent)

    # Create threads for both components
    listener_thread = threading.Thread(
        target=run_email_listener,
        args=(email_listener,),
        daemon=True
    )
    chatbot_thread = threading.Thread(
        target=run_chatbot,
        args=(agent,),
        daemon=True
    )

    # Start both threads
    listener_thread.start()
    chatbot_thread.start()

    try:
        # Keep the main thread alive
        while True:
            listener_thread.join(1)
            chatbot_thread.join(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
