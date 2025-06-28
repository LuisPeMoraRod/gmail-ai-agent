from composio_langgraph import Action, ComposioToolSet, App


class GmailIntegrator:
    def __init__(self, integration_id: str, user_id: str):
        self.toolset = ComposioToolSet()
        self.integration_id = integration_id
        self.user_id = user_id
        self.entity = self.toolset.get_entity(user_id)

        try:
            connection_request = self.initiate_connection()
            self.wait_for_activation(connection_request)

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
            active_connection = connection_request.wait_until_active(
                client=self.toolset.client,  # Pass the Composio client instance
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
            # Implement retry logic or inform the user
