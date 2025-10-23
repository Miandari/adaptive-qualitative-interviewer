"""
Prompt building utilities for ESM conversations
"""
from typing import Dict, Any, List


class ESMPromptBuilder:
    """
    Builds prompts for ESM conversations based on experiment configuration.
    """

    def __init__(self, experiment_config: Dict[str, Any]):
        """
        Initialize with experiment configuration.

        Args:
            experiment_config: Loaded experiment configuration
        """
        self.config = experiment_config

    def build_initial_greeting(self) -> str:
        """
        Build the initial greeting message.

        Returns:
            Formatted greeting message
        """
        initial_q = self.config.get("initial_question", {})
        context = initial_q.get("context", "")
        question = initial_q.get("text", "")

        if context:
            return f"{context}\n\n{question}"
        return question

    def build_system_prompt(
        self,
        topics_covered: List[str],
        exchange_count: int,
        next_focus: str
    ) -> str:
        """
        Build a system prompt for the conversation.

        Args:
            topics_covered: List of topics already discussed
            exchange_count: Number of exchanges so far
            next_focus: What to focus on next

        Returns:
            Formatted system prompt
        """
        guidelines = self.config.get("conversation_guidelines", {})
        goals = self.config.get("goals", [])

        tone = guidelines.get("tone", "warm and curious")
        style = guidelines.get("style", "conversational")
        approach = guidelines.get("approach", "")

        prompt = f"""You are a research assistant conducting an ESM study about {self.config.get('name', 'social interactions')}.

CONVERSATION STYLE:
- Tone: {tone}
- Style: {style}

RESEARCH GOALS:
{self._format_list(goals)}

{approach}

CURRENT STATUS:
- Exchanges: {exchange_count}
- Topics covered: {', '.join(topics_covered) if topics_covered else 'None yet'}
- Next focus: {next_focus}

Ask ONE relevant follow-up question that explores the next focus area naturally."""

        return prompt

    def build_closing_message(self) -> str:
        """
        Build a closing message for the conversation.

        Returns:
            Formatted closing message
        """
        return (
            "Thank you so much for sharing your experience with me. "
            "Your responses will help us better understand social interactions and empathy. "
            "Have a wonderful day!"
        )

    def _format_list(self, items: List[str]) -> str:
        """Format a list of items as bullet points"""
        return "\n".join(f"- {item}" for item in items)

    def get_follow_up_suggestions(self, category: str) -> List[str]:
        """
        Get example follow-up questions for a category.

        Args:
            category: Category name (e.g., "perspective_taking")

        Returns:
            List of example questions
        """
        categories = self.config.get("follow_up_categories", {})
        cat_info = categories.get(category, {})
        return cat_info.get("example_questions", [])
