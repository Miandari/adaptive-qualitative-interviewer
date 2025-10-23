"""
Conversation state management for LangGraph
"""
from typing import TypedDict, Annotated, Sequence, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ConversationState(TypedDict):
    """
    State schema for the ESM conversation flow.

    This state is passed between nodes in the LangGraph and maintains
    all necessary context for dynamic conversation management.
    """

    # Message history with automatic accumulation
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # Session information
    session_id: str
    participant_id: str
    experiment_id: str
    user_info: Dict[str, Any]  # Additional user demographics/info

    # Conversation tracking
    exchange_count: int  # Number of back-and-forth exchanges
    topics_covered: list[str]  # Track which areas have been explored

    # Experiment configuration
    experiment_config: Dict[str, Any]  # Loaded from YAML

    # Conversation control
    should_continue: bool  # Whether to continue the conversation
    current_stage: str  # Current stage: "initial", "exploration", "closing"

    # Context from previous exchanges
    conversation_context: str  # Summary of key points discussed
    participant_responses: list[Dict[str, Any]]  # Structured response data


def create_initial_state(
    session_id: str,
    participant_id: str,
    experiment_id: str,
    user_info: Dict[str, Any],
    experiment_config: Dict[str, Any]
) -> ConversationState:
    """
    Create the initial conversation state

    Args:
        session_id: Unique session identifier
        participant_id: Participant identifier
        experiment_id: Experiment identifier
        user_info: User demographic information
        experiment_config: Loaded experiment configuration

    Returns:
        Initial conversation state
    """
    return ConversationState(
        messages=[],
        session_id=session_id,
        participant_id=participant_id,
        experiment_id=experiment_id,
        user_info=user_info,
        exchange_count=0,
        topics_covered=[],
        experiment_config=experiment_config,
        should_continue=True,
        current_stage="initial",
        conversation_context="",
        participant_responses=[]
    )
