"""
Example: Using ESM Chatbot as a standalone Python library

This demonstrates how to use the ESMBot directly in your Python code.
"""
from core.api import ESMBot


def main():
    """Run a simple conversation example"""

    # Initialize the bot
    print("Initializing ESM Chatbot...")
    bot = ESMBot()

    # List available experiments
    experiments = bot.list_experiments()
    print(f"\nAvailable experiments: {experiments}")

    if not experiments:
        print("No experiments found. Please configure experiments.yaml")
        return

    # Use the first experiment
    experiment_id = experiments[0]
    print(f"\nStarting experiment: {experiment_id}")

    # Start a session
    session = bot.start_session(
        participant_id="test_user_001",
        experiment_id=experiment_id,
        user_info={
            "participant_id": "test_user_001",
            "age": 25,
            "timezone": "UTC"
        }
    )

    print(f"Session started: {session.session_id}")

    # Get initial message
    initial_msg = bot.get_initial_message(session.session_id)
    print(f"\nBot: {initial_msg}")

    # Simulate conversation
    user_messages = [
        "I had a conversation with my colleague today about a project deadline.",
        "It was in the office, lasted about 20 minutes.",
        "My colleague seemed stressed about the timeline.",
        "I tried to listen and understand their concerns about the workload.",
        "I felt empathetic towards their situation."
    ]

    for user_msg in user_messages:
        print(f"\nUser: {user_msg}")

        # Process message
        result = bot.process_message(
            session_id=session.session_id,
            message=user_msg
        )

        print(f"Bot: {result['response']}")
        print(f"[Exchange {result['exchange_count']}, Topics: {', '.join(result['topics_covered'])}]")

        # Check if complete
        if result['is_complete']:
            print("\n=== Conversation Complete ===")
            break

    # Export session data
    print(f"\nExporting session data...")
    data = bot.export_session(session.session_id)

    # Save to file
    import json
    import os

    os.makedirs("exports", exist_ok=True)
    filename = f"exports/example_session_{session.session_id}.json"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Session data exported to: {filename}")


if __name__ == "__main__":
    main()
