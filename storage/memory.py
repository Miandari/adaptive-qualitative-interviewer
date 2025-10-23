"""
In-memory storage for conversation data and session information.

This is a simple storage adapter for development and testing.
Can be replaced with database adapters later.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class InMemoryStorage:
    """
    Simple in-memory storage for ESM chatbot data.

    Stores conversation history, session data, and responses.
    Data is lost when the application restarts.
    """

    def __init__(self):
        """Initialize empty storage"""
        self._conversations: Dict[str, List[Dict[str, Any]]] = {}
        self._session_data: Dict[str, Dict[str, Any]] = {}
        self._responses: Dict[str, List[Dict[str, Any]]] = {}

    def store_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Store a conversation message.

        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata about the message
        """
        if session_id not in self._conversations:
            self._conversations[session_id] = []

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self._conversations[session_id].append(message)

    def get_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all messages for a session.

        Args:
            session_id: Session identifier

        Returns:
            List of messages
        """
        return self._conversations.get(session_id, [])

    def store_session_data(self, session_id: str, data: Dict[str, Any]):
        """
        Store session metadata.

        Args:
            session_id: Session identifier
            data: Session data to store
        """
        self._session_data[session_id] = data

    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session metadata.

        Args:
            session_id: Session identifier

        Returns:
            Session data if found, None otherwise
        """
        return self._session_data.get(session_id)

    def store_response(
        self,
        session_id: str,
        question: str,
        answer: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Store a structured question-answer pair.

        Args:
            session_id: Session identifier
            question: Question asked
            answer: Participant's answer
            metadata: Optional metadata
        """
        if session_id not in self._responses:
            self._responses[session_id] = []

        response = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self._responses[session_id].append(response)

    def get_responses(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all structured responses for a session.

        Args:
            session_id: Session identifier

        Returns:
            List of question-answer pairs
        """
        return self._responses.get(session_id, [])

    def export_session(self, session_id: str) -> Dict[str, Any]:
        """
        Export all data for a session.

        Args:
            session_id: Session identifier

        Returns:
            Complete session data including conversation and responses
        """
        return {
            "session_id": session_id,
            "session_data": self.get_session_data(session_id),
            "conversation": self.get_conversation(session_id),
            "responses": self.get_responses(session_id),
            "exported_at": datetime.now().isoformat()
        }

    def export_all_sessions(self) -> List[Dict[str, Any]]:
        """
        Export all sessions.

        Returns:
            List of all session data
        """
        all_session_ids = set(
            list(self._conversations.keys()) +
            list(self._session_data.keys()) +
            list(self._responses.keys())
        )

        return [self.export_session(sid) for sid in all_session_ids]

    def save_to_file(self, filepath: str):
        """
        Save all data to a JSON file.

        Args:
            filepath: Path to save the file
        """
        data = {
            "conversations": self._conversations,
            "session_data": self._session_data,
            "responses": self._responses,
            "exported_at": datetime.now().isoformat()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def clear(self):
        """Clear all stored data"""
        self._conversations.clear()
        self._session_data.clear()
        self._responses.clear()
