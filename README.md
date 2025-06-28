# Generalist Trigger for Gmail AI Agent

This project implements an AI Agent using LangGraph and integrates it with Gmail using Composio to respond to emails on your behalf. The agent can also be used as a chatbot in the console.

## Prerequisites

1. An Anthropic API key.
2. A Composio API key.
3. A Gmail integration ID from Composio. Follow the instructions in the [Composio documentation](https://docs.composio.dev/auth/set-up-integrations) to set up the Gmail integration and get the ID.

## Setup

1. Create a `.env` file in the root directory of the project with the following content:

   ```plaintext
   ANTHROPIC_API_KEY='your_anthropic_api_key'
   COMPOSIO_API_KEY='your_composio_api_key'
   GMAIL_INTEGRATION_ID='your_gmail_integration_id'
   ```

2. Create a virtual environment and install the required dependencies:
   ```bash
    uv venv
    source .venv/bin/activate
    uv add -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   python src/main.py
   ```

2. Authorize the Gmail integration when prompted. This will allow the application to access your Gmail account.

3. The application will start listening for new emails and respond to them using the AI agent. You can also interact with the chatbot through the console.

## Demo

The following video demonstrates the functionality of the Gmail AI Agent:
[![Demo Video](https://drive.google.com/file/d/1EJ53TpSYHZeW8478WH_ESBNXxM8qVg5H/view?usp=sharing)
