from typing import Protocol
from gmail_integrator import GmailIntegrator


class EmailHandler(Protocol):
    def answer_email(self, sender: str, email_text: str, thread_id: str) -> None:
        ...


class EmailListener:
    """
    A class to handle email listening functionality.
    """
    TRIGGER_NAME = "GMAIL_NEW_GMAIL_MESSAGE"

    def __init__(self, gmail_integrator: GmailIntegrator, email_handler: EmailHandler):
        self.gmail_integrator = gmail_integrator
        self.email_handler = email_handler
        self.listener = self.gmail_integrator.toolset.create_trigger_listener()

    def setup_listener(self):
        """
        Set up the email listener with callback.
        """
        @self.listener.callback(
            filters={
                "trigger_name": self.TRIGGER_NAME,
            }
        )
        def handle_trigger(event):
            print("Received trigger event...")
            payload = event.payload

            sender = payload.get("sender", "")
            email_text = payload.get("message_text", "")
            thread_id = payload.get("thread_id", "")

            self.email_handler.answer_email(
                sender=sender,
                email_text=email_text,
                thread_id=thread_id
            )

    def start(self):
        """
        Start listening for email events.
        """
        self.setup_listener()
        self.listener.wait_forever()
