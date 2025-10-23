"""
Example: Using ESM Chatbot via REST API

This demonstrates how to integrate with the chatbot using HTTP requests.
Requires the FastAPI server to be running.
"""
import requests
import json


class ESMChatbotClient:
    """Simple client for the ESM Chatbot REST API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def list_experiments(self):
        """List available experiments"""
        response = requests.get(f"{self.base_url}/experiments")
        response.raise_for_status()
        return response.json()

    def get_experiment(self, experiment_id: str):
        """Get experiment details"""
        response = requests.get(f"{self.base_url}/experiments/{experiment_id}")
        response.raise_for_status()
        return response.json()

    def start_session(self, participant_id: str, experiment_id: str, user_info: dict):
        """Start a new session"""
        response = requests.post(
            f"{self.base_url}/sessions/start",
            json={
                "participant_id": participant_id,
                "experiment_id": experiment_id,
                "user_info": user_info
            }
        )
        response.raise_for_status()
        return response.json()

    def send_message(self, session_id: str, message: str):
        """Send a message"""
        response = requests.post(
            f"{self.base_url}/messages",
            json={
                "session_id": session_id,
                "message": message
            }
        )
        response.raise_for_status()
        return response.json()

    def get_session(self, session_id: str):
        """Get session information"""
        response = requests.get(f"{self.base_url}/sessions/{session_id}")
        response.raise_for_status()
        return response.json()

    def export_session(self, session_id: str):
        """Export session data"""
        response = requests.get(f"{self.base_url}/sessions/{session_id}/export")
        response.raise_for_status()
        return response.json()


def main():
    """Example usage of the API client"""

    # Initialize client
    client = ESMChatbotClient()

    print("ESM Chatbot API Client Example")
    print("=" * 50)

    # Check health
    try:
        response = requests.get(f"{client.base_url}/health")
        print(f"\nAPI Status: {response.json()['status']}")
    except Exception as e:
        print(f"\nError: Could not connect to API. Make sure the server is running.")
        print(f"Start the server with: uvicorn interfaces.fastapi_app:app --reload")
        return

    # List experiments
    experiments = client.list_experiments()
    print(f"\nAvailable experiments: {experiments}")

    if not experiments:
        print("No experiments configured.")
        return

    # Get experiment details
    experiment_id = experiments[0]
    exp_info = client.get_experiment(experiment_id)
    print(f"\nExperiment: {exp_info['name']}")
    print(f"Description: {exp_info['description']}")

    # Start session
    session_data = client.start_session(
        participant_id="api_user_001",
        experiment_id=experiment_id,
        user_info={
            "participant_id": "api_user_001",
            "age": 30
        }
    )

    session_id = session_data['session_id']
    print(f"\nSession started: {session_id}")
    print(f"\nBot: {session_data['initial_message']}")

    # Simulate conversation
    messages = [
        "I talked with my friend yesterday about her new job.",
        "She seemed really excited about the opportunity.",
        "I could tell from her tone and the way she was describing it."
    ]

    for msg in messages:
        print(f"\nUser: {msg}")

        result = client.send_message(session_id, msg)
        print(f"Bot: {result['response']}")

        if result['is_complete']:
            print("\n=== Conversation Complete ===")
            break

    # Export session
    print(f"\nExporting session data...")
    export_data = client.export_session(session_id)

    # Save to file
    import os
    os.makedirs("exports", exist_ok=True)
    filename = f"exports/api_session_{session_id}.json"

    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"Session data exported to: {filename}")


if __name__ == "__main__":
    main()
