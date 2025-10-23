"""
Conversation nodes for the LangGraph flow
"""
from typing import Dict, Any, Callable
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from .state import ConversationState
from .edges import determine_next_question_focus


def create_conversation_nodes(llm: BaseChatModel) -> Dict[str, Callable]:
    """
    Create conversation node functions with the provided LLM.

    Args:
        llm: Language model instance to use for generation

    Returns:
        Dictionary of node functions
    """

    def initial_question_node(state: ConversationState) -> Dict[str, Any]:
        """
        Start the conversation with the initial probe question.

        This node initiates the ESM interaction by asking the configured
        initial question from the experiment setup.
        """
        experiment_config = state["experiment_config"]
        initial_q = experiment_config.get("initial_question", {})

        question_text = initial_q.get("text", "Can you tell me about a recent interaction you had with another person?")
        context = initial_q.get("context", "")

        # Create greeting message
        greeting = f"{context}\n\n{question_text}" if context else question_text

        return {
            "messages": [AIMessage(content=greeting)],
            "exchange_count": state["exchange_count"] + 1,
            "current_stage": "exploration"
        }

    def conversation_node(state: ConversationState) -> Dict[str, Any]:
        """
        Main conversation node that generates dynamic follow-up questions.

        This node analyzes the participant's response and generates
        contextually relevant follow-up questions based on the experiment
        goals and what has been covered so far.
        """
        experiment_config = state["experiment_config"]
        guidelines = experiment_config.get("conversation_guidelines", {})

        # Determine what to focus on next
        next_focus = determine_next_question_focus(state)

        # Build system prompt
        system_prompt = _build_system_prompt(state, next_focus)

        # Get recent conversation history (last 6 messages to keep context manageable)
        recent_messages = state["messages"][-6:] if len(state["messages"]) > 6 else state["messages"]

        # Prepare messages for LLM
        messages = [SystemMessage(content=system_prompt)] + list(recent_messages)

        # Generate response
        response = llm.invoke(messages)

        # Update topics covered based on response (simple keyword matching)
        updated_topics = _update_topics_covered(state, response.content)

        return {
            "messages": [response],
            "exchange_count": state["exchange_count"] + 1,
            "topics_covered": updated_topics,
            "conversation_context": _update_context(state, response.content)
        }

    def closing_node(state: ConversationState) -> Dict[str, Any]:
        """
        Close the conversation gracefully.

        Provides a thank you message and any closing instructions.
        """
        closing_message = (
            "Thank you so much for sharing about your interaction with me. "
            "Your responses will help us better understand empathy in daily social interactions. "
            "Have a great day!"
        )

        return {
            "messages": [AIMessage(content=closing_message)],
            "current_stage": "closing",
            "should_continue": False
        }

    return {
        "initial_question": initial_question_node,
        "conversation": conversation_node,
        "closing": closing_node
    }


def _build_system_prompt(state: ConversationState, next_focus: str) -> str:
    """Build the system prompt for the conversation node"""
    experiment_config = state["experiment_config"]
    guidelines = experiment_config.get("conversation_guidelines", {})
    goals = experiment_config.get("goals", [])
    follow_up_cats = experiment_config.get("follow_up_categories", {})

    tone = guidelines.get("tone", "warm and curious")
    style = guidelines.get("style", "conversational")
    approach = guidelines.get("approach", "")

    topics_covered = state.get("topics_covered", [])
    exchange_count = state.get("exchange_count", 0)

    prompt = f"""You are a research assistant conducting an experience sampling study about {experiment_config.get('name', 'social interactions')}.

{experiment_config.get('description', '')}

CONVERSATION STYLE:
- Tone: {tone}
- Style: {style}

RESEARCH GOALS:
{chr(10).join(f"- {goal}" for goal in goals)}

APPROACH:
{approach}

FOLLOW-UP CATEGORIES YOU CAN EXPLORE:
{_format_follow_up_categories(follow_up_cats)}

CURRENT STATUS:
- Exchanges so far: {exchange_count}
- Topics covered: {', '.join(topics_covered) if topics_covered else 'None yet'}
- Next focus area: {next_focus}

INSTRUCTIONS:
Based on the participant's most recent response, ask ONE relevant follow-up question that:
1. Relates naturally to what they just shared
2. Helps explore the next focus area: "{next_focus}"
3. Is open-ended when possible to encourage detailed responses
4. Shows genuine curiosity about the specifics they mentioned

Keep your question concise and conversational. Do not include explanations or multiple questions."""

    return prompt


def _format_follow_up_categories(categories: Dict[str, Any]) -> str:
    """Format follow-up categories for the prompt"""
    formatted = []
    for cat_name, cat_info in categories.items():
        desc = cat_info.get("description", "")
        examples = cat_info.get("example_questions", [])
        formatted.append(f"\n{cat_name.replace('_', ' ').title()}: {desc}")
        if examples:
            formatted.append("  Examples: " + "; ".join(examples[:2]))

    return "\n".join(formatted)


def _update_topics_covered(state: ConversationState, response: str) -> list[str]:
    """Update the list of topics covered based on the response"""
    topics = state.get("topics_covered", []).copy()
    response_lower = response.lower()

    # Simple keyword matching to identify topics
    topic_keywords = {
        "context": ["where", "when", "how long", "place", "time"],
        "perspective": ["perspective", "think", "feel", "view", "understand"],
        "emotion": ["emotion", "feeling", "felt", "mood"],
        "communication": ["communication", "listen", "talk", "conversation", "said"]
    }

    for topic, keywords in topic_keywords.items():
        if topic not in topics and any(kw in response_lower for kw in keywords):
            topics.append(topic)

    return topics


def _update_context(state: ConversationState, new_content: str) -> str:
    """Update the conversation context summary"""
    existing_context = state.get("conversation_context", "")

    # For now, just keep track of recent topics
    # In a more advanced version, could use LLM to summarize
    if existing_context:
        return existing_context

    return "Conversation in progress"
