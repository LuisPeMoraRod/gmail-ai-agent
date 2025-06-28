from composio_langgraph import Action, ComposioToolSet, App


class GmailIntegrator:
    """
    A class to handle Gmail integration using Composio's toolset.
    It uses OAuth to connect to a user's Gmail account and activates a trigger to listen for new emails.
    It also provides a method to reply to a Gmail thread that can be used by the AI agent.
    """

    def __init__(self, integration_id: str, user_id: str):
        self.toolset = ComposioToolSet()
        self.integration_id = integration_id
        self.user_id = user_id
        self.entity = self.toolset.get_entity(user_id)
        self.active_connection = None

        try:
            connection_request = self.initiate_connection()
            self.wait_for_activation(connection_request)
            self.enable_trigger()

        except Exception as e:
            print(f"Error connecting to Gmail: {e}")

    def initiate_connection(self):
        """
        Initiates the OAuth connection for the Gmail integration.
        Returns a connection request object.
        """
        try:
            print(f"Initiating OAuth connection...\n")
            connection_request = self.toolset.initiate_connection(
                integration_id=self.integration_id,
                entity_id=self.user_id,
                app=App.GMAIL,
            )
            # Check if a redirect URL was provided (expected for OAuth)
            if connection_request.redirectUrl:
                print(
                    f"Please, authorize the application by visiting: {connection_request.redirectUrl}\n"
                )
                return connection_request
            else:
                raise ValueError(
                    "Expected a redirectUrl for OAuth flow but didn't receive one. \nMaybe the integration is misconfigured?"
                )
        except Exception as e:
            print(f"Error initiating connection: {e}")

    def wait_for_activation(self, connection_request, timeout=180):
        """
        Waits for the connection to become active.
        Polls Composio until the status is ACTIVE or timeout is reached.
        """
        print("Waiting for user authorization and connection activation...")
        try:
            # Poll Composio until the status is ACTIVE
            self.active_connection = connection_request.wait_until_active(
                client=self.toolset.client,
                timeout=timeout,
            )

            try:
                action = Action.GMAIL_GET_PROFILE
                user_info = self.toolset.execute_action(
                    action=action, entity_id=self.user_id, params={}
                )
                print(
                    f"Connection was successfull! User email address: {user_info['data']['response_data']['emailAddress']}\n"
                )
            except Exception as e:
                print(f"Error fetching user profile: {e}")

        except Exception as e:
            print(f"Connection did not become active within timeout or failed: {e}")

    def enable_trigger(self):
        """
        Enable the trigger for the Gmail integration.
        """
        try:
            res = self.entity.enable_trigger(
                app=App.GMAIL, trigger_name="GMAIL_NEW_GMAIL_MESSAGE", config={}
            )
            if res["status"] != "success":
                raise Exception(f"Failed to enable trigger: {res['message']}")
        except Exception as e:
            print(f"Error enabling trigger: {e}")

    def reply_to_thread(self, recipient_email: str, message_text: str, thread_id: str):
        """
        Reply to a Gmail thread.
        """
        try:
            action = Action.GMAIL_REPLY_TO_THREAD
            response = self.toolset.execute_action(
                action=action,
                entity_id=self.user_id,
                params={
                    "recipient_email": recipient_email,
                    "message_body": message_text,
                    "thread_id": thread_id,
                },
            )
        except Exception as e:
            print(f"Error replying to thread: {e}")
