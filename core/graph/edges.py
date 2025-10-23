"""
Conditional edges for conversation flow control
"""
from typing import Literal
from .state import ConversationState


def should_continue_conversation(state: ConversationState) -> Literal["continue", "end"]:
    """
    Determine whether to continue the conversation or end it.

    This function evaluates the current state and decides the next action
    based on conversation goals and exit criteria.

    Args:
        state: Current conversation state

    Returns:
        "continue" to keep the conversation going, "end" to terminate
    """

    # Check explicit continuation flag
    if not state.get("should_continue", True):
        return "end"

    # Get exit criteria from experiment config
    experiment_config = state.get("experiment_config", {})
    guidelines = experiment_config.get("conversation_guidelines", {})
    exit_criteria = guidelines.get("exit_criteria", [])

    exchange_count = state.get("exchange_count", 0)
    topics_covered = state.get("topics_covered", [])
    goals = experiment_config.get("goals", [])

    # Check if maximum exchanges reached
    # First check user preference (if provided)
    user_info = state.get("user_info", {})
    depth_preference = user_info.get("conversation_depth", "")

    max_exchanges = 8  # default

    # Parse depth preference
    if "Short" in depth_preference or "5" in depth_preference:
        max_exchanges = 5
    elif "Medium" in depth_preference or "8" in depth_preference:
        max_exchanges = 8
    elif "Deep" in depth_preference or "12" in depth_preference:
        max_exchanges = 12
    else:
        # Fall back to exit criteria
        for criterion in exit_criteria:
            if "exchanges completed" in criterion:
                # Extract number from criterion string
                import re
                match = re.search(r'(\d+)', criterion)
                if match:
                    max_exchanges = int(match.group(1))

    if exchange_count >= max_exchanges:
        return "end"

    # Check if all main goals are covered
    if len(topics_covered) >= len(goals):
        return "end"

    # Check if we're in closing stage
    current_stage = state.get("current_stage", "initial")
    if current_stage == "closing":
        return "end"

    # Continue the conversation
    return "continue"


def determine_next_question_focus(state: ConversationState) -> str:
    """
    Determine what aspect to focus on for the next question.

    This helps guide the LLM to ask relevant follow-up questions
    based on what has already been covered.

    Args:
        state: Current conversation state

    Returns:
        Focus area for next question
    """
    topics_covered = state.get("topics_covered", [])
    goals = state.get("experiment_config", {}).get("goals", [])

    # Identify uncovered goals
    uncovered = []
    for goal in goals:
        is_covered = any(topic in goal.lower() for topic in topics_covered)
        if not is_covered:
            uncovered.append(goal)

    if uncovered:
        return uncovered[0]

    # If all covered, we can do deeper exploration
    return "deeper exploration of mentioned topics"
