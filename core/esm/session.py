"""
Session management for ESM chatbot
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class SessionInfo(BaseModel):
    """Information about a user session"""

    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    participant_id: str
    experiment_id: str
    user_info: Dict[str, Any] = Field(default_factory=dict)
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    is_active: bool = True

    # Conversation metadata
    total_exchanges: int = 0
    total_messages: int = 0

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionManager:
    """
    Manages user sessions for the ESM chatbot.

    This class handles session creation, retrieval, and storage
    of session information.
    """

    def __init__(self):
        """Initialize the session manager with in-memory storage"""
        self._sessions: Dict[str, SessionInfo] = {}

    def create_session(
        self,
        participant_id: str,
        experiment_id: str,
        user_info: Optional[Dict[str, Any]] = None
    ) -> SessionInfo:
        """
        Create a new session for a participant.

        Args:
            participant_id: Unique identifier for the participant
            experiment_id: Identifier for the experiment
            user_info: Additional user demographic/context information

        Returns:
            Created session information
        """
        session = SessionInfo(
            participant_id=participant_id,
            experiment_id=experiment_id,
            user_info=user_info or {}
        )

        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session information if found, None otherwise
        """
        return self._sessions.get(session_id)

    def update_session(self, session_id: str, **kwargs) -> Optional[SessionInfo]:
        """
        Update session information.

        Args:
            session_id: Session identifier
            **kwargs: Fields to update

        Returns:
            Updated session information if found, None otherwise
        """
        session = self._sessions.get(session_id)
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
        return session

    def end_session(self, session_id: str) -> Optional[SessionInfo]:
        """
        Mark a session as ended.

        Args:
            session_id: Session identifier

        Returns:
            Updated session information if found, None otherwise
        """
        session = self._sessions.get(session_id)
        if session:
            session.end_time = datetime.now()
            session.is_active = False
        return session

    def get_all_sessions(self, experiment_id: Optional[str] = None) -> list[SessionInfo]:
        """
        Get all sessions, optionally filtered by experiment.

        Args:
            experiment_id: Optional experiment ID to filter by

        Returns:
            List of sessions
        """
        sessions = list(self._sessions.values())
        if experiment_id:
            sessions = [s for s in sessions if s.experiment_id == experiment_id]
        return sessions

    def clear_sessions(self):
        """Clear all sessions (useful for testing)"""
        self._sessions.clear()
