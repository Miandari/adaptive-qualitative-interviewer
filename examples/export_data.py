"""
Utility script for exporting ESM chatbot data to various formats

Usage:
    python examples/export_data.py --format json
    python examples/export_data.py --format csv --output results.csv
"""
import argparse
import json
import csv
from datetime import datetime
from pathlib import Path
from storage.memory import InMemoryStorage


def export_to_json(data: dict, output_file: str):
    """Export data to JSON format"""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Exported to JSON: {output_file}")


def export_to_csv(sessions: list, output_file: str):
    """Export sessions to CSV format"""
    if not sessions:
        print("No sessions to export")
        return

    # Flatten session data for CSV
    rows = []
    for session in sessions:
        session_data = session.get('session_data', {})
        conversation = session.get('conversation', [])
        responses = session.get('responses', [])

        # Create a row for each message exchange
        for i, msg in enumerate(conversation):
            row = {
                'session_id': session.get('session_id', ''),
                'participant_id': session_data.get('participant_id', ''),
                'experiment_id': session_data.get('experiment_id', ''),
                'message_number': i + 1,
                'role': msg.get('role', ''),
                'content': msg.get('content', ''),
                'timestamp': msg.get('timestamp', '')
            }

            # Add user info
            user_info = session_data.get('user_info', {})
            for key, value in user_info.items():
                row[f'user_{key}'] = value

            rows.append(row)

    # Write to CSV
    if rows:
        fieldnames = rows[0].keys()
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Exported to CSV: {output_file}")


def export_responses_to_csv(sessions: list, output_file: str):
    """Export structured responses to CSV"""
    rows = []

    for session in sessions:
        session_data = session.get('session_data', {})
        responses = session.get('responses', [])

        for i, resp in enumerate(responses):
            row = {
                'session_id': session.get('session_id', ''),
                'participant_id': session_data.get('participant_id', ''),
                'experiment_id': session_data.get('experiment_id', ''),
                'response_number': i + 1,
                'question': resp.get('question', ''),
                'answer': resp.get('answer', ''),
                'timestamp': resp.get('timestamp', '')
            }

            # Add user info
            user_info = session_data.get('user_info', {})
            for key, value in user_info.items():
                row[f'user_{key}'] = value

            rows.append(row)

    if rows:
        fieldnames = rows[0].keys()
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Exported responses to CSV: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Export ESM chatbot data')
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'responses_csv'],
        default='json',
        help='Export format'
    )
    parser.add_argument(
        '--output',
        help='Output file path',
        default=None
    )
    parser.add_argument(
        '--data-file',
        help='Input data file (JSON)',
        default=None
    )

    args = parser.parse_args()

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = 'json' if args.format == 'json' else 'csv'
        output_file = f"exports/export_{timestamp}.{ext}"

    # Ensure exports directory exists
    Path("exports").mkdir(exist_ok=True)

    # Load data
    if args.data_file:
        with open(args.data_file, 'r') as f:
            data = json.load(f)

        # If it's raw storage format, convert it
        if 'conversations' in data:
            # Convert storage format to session format
            sessions = []
            for session_id in data['conversations'].keys():
                sessions.append({
                    'session_id': session_id,
                    'session_data': data['session_data'].get(session_id, {}),
                    'conversation': data['conversations'].get(session_id, []),
                    'responses': data['responses'].get(session_id, [])
                })
        else:
            # Assume it's already in session format
            sessions = data if isinstance(data, list) else [data]
    else:
        print("Note: No data file specified. This example shows export format structure.")
        print("To export actual data, provide --data-file option")

        # Create example data
        sessions = [{
            'session_id': 'example_session_001',
            'session_data': {
                'participant_id': 'participant_001',
                'experiment_id': 'empathy_study',
                'user_info': {'age': 25, 'timezone': 'UTC'}
            },
            'conversation': [
                {'role': 'assistant', 'content': 'Hello! Tell me about a recent interaction.', 'timestamp': '2025-01-01T10:00:00'},
                {'role': 'user', 'content': 'I talked with my colleague today.', 'timestamp': '2025-01-01T10:00:30'}
            ],
            'responses': []
        }]

    # Export based on format
    if args.format == 'json':
        export_to_json(sessions, output_file)
    elif args.format == 'csv':
        export_to_csv(sessions, output_file)
    elif args.format == 'responses_csv':
        export_responses_to_csv(sessions, output_file)

    print(f"\nExport complete!")


if __name__ == "__main__":
    main()
