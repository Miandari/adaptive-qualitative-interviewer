"""
Core API for the ESM Chatbot.

This module provides the main interface that can be used by different
front-ends (Chainlit, FastAPI, etc.) or imported as a library.
"""
from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .graph.state import ConversationState, create_initial_state
from .graph.nodes import create_conversation_nodes
from .graph.edges import should_continue_conversation
from .esm.session import SessionManager, SessionInfo
from .esm.questions import QuestionManager
from storage.memory import InMemoryStorage
from config.settings import get_settings


class ESMBot:
    """
    Main ESM Chatbot class.

    This class orchestrates the conversation flow using LangGraph
    and can be used as a standalone library or through UI interfaces.
    """

    def __init__(
        self,
        experiment_config_path: Optional[str] = None,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None
    ):
        """
        Initialize the ESM Bot.

        Args:
            experiment_config_path: Path to experiments YAML file
            llm_provider: LLM provider (openai or anthropic)
            llm_model: Model name to use
        """
        self.settings = get_settings()

        # Initialize components
        self.session_manager = SessionManager()
        self.storage = InMemoryStorage()

        config_path = experiment_config_path or self.settings.experiment_config_path
        self.question_manager = QuestionManager(config_path)

        # Initialize LLM
        provider = llm_provider or self.settings.llm_provider
        model = llm_model or self.settings.llm_model

        if provider == "openai":
            self.llm = ChatOpenAI(
                model=model,
                temperature=self.settings.temperature
            )
        elif provider == "anthropic":
            self.llm = ChatAnthropic(
                model=model,
                temperature=self.settings.temperature
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        # Build the conversation graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph conversation flow"""

        # Create the graph
        workflow = StateGraph(ConversationState)

        # Create nodes
        nodes = create_conversation_nodes(self.llm)

        # Add nodes to the graph
        workflow.add_node("initial_question", nodes["initial_question"])
        workflow.add_node("conversation", nodes["conversation"])
        workflow.add_node("closing", nodes["closing"])

        # Define routing function to decide where to start
        def route_start(state: ConversationState):
            # If no messages (or only system messages), start with initial question
            user_messages = [m for m in state.get("messages", []) if hasattr(m, 'type') and m.type == "human"]
            if len(user_messages) == 0 and state.get("exchange_count", 0) == 0:
                return "initial_question"
            return "conversation"

        # Add conditional edge from START
        workflow.add_conditional_edges(
            START,
            route_start,
            {
                "initial_question": "initial_question",
                "conversation": "conversation"
            }
        )

        # Initial question goes to END (waits for user response)
        workflow.add_edge("initial_question", END)

        # Conditional edge from conversation
        workflow.add_conditional_edges(
            "conversation",
            should_continue_conversation,
            {
                "continue": END,  # Wait for next user message
                "end": "closing"  # Move to closing
            }
        )

        workflow.add_edge("closing", END)

        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    def start_session(
        self,
        participant_id: str,
        experiment_id: str,
        user_info: Optional[Dict[str, Any]] = None
    ) -> SessionInfo:
        """
        Start a new conversation session.

        Args:
            participant_id: Participant identifier
            experiment_id: Experiment identifier
            user_info: Additional user information

        Returns:
            Session information

        Raises:
            ValueError: If experiment not found or user info invalid
        """
        # Validate experiment exists
        config = self.question_manager.get_experiment_config(experiment_id)
        if not config:
            raise ValueError(f"Experiment '{experiment_id}' not found")

        # Validate user info
        is_valid, missing = self.question_manager.validate_user_info(
            experiment_id,
            user_info or {}
        )
        if not is_valid:
            raise ValueError(f"Missing required user info fields: {', '.join(missing)}")

        # Create session
        session = self.session_manager.create_session(
            participant_id=participant_id,
            experiment_id=experiment_id,
            user_info=user_info or {}
        )

        # Store session data
        self.storage.store_session_data(session.session_id, {
            "participant_id": participant_id,
            "experiment_id": experiment_id,
            "user_info": user_info or {},
            "start_time": session.start_time.isoformat()
        })

        return session

    def process_message(
        self,
        session_id: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response.

        Args:
            session_id: Session identifier
            message: User's message

        Returns:
            Dictionary containing response and metadata

        Raises:
            ValueError: If session not found
        """
        # Get session
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")

        # Get experiment config
        config = self.question_manager.get_experiment_config(session.experiment_id)

        # Store user message
        self.storage.store_message(session_id, "user", message)

        # Get or create state
        state = self._get_or_create_state(session, config)

        # Add user message to state
        state["messages"].append(HumanMessage(content=message))

        # Run the graph
        thread_config = {"configurable": {"thread_id": session_id}}
        result = self.graph.invoke(state, thread_config)

        # Extract assistant response
        last_message = result["messages"][-1]
        response_text = last_message.content

        # Store assistant message
        self.storage.store_message(session_id, "assistant", response_text)

        # Update session
        self.session_manager.update_session(
            session_id,
            total_exchanges=result.get("exchange_count", 0),
            total_messages=len(result["messages"])
        )

        # Check if conversation ended
        if not result.get("should_continue", True):
            self.session_manager.end_session(session_id)

        return {
            "response": response_text,
            "session_id": session_id,
            "exchange_count": result.get("exchange_count", 0),
            "is_complete": not result.get("should_continue", True),
            "topics_covered": result.get("topics_covered", [])
        }

    def get_initial_message(self, session_id: str) -> str:
        """
        Get the initial greeting message for a session.

        Args:
            session_id: Session identifier

        Returns:
            Initial greeting message
        """
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")

        config = self.question_manager.get_experiment_config(session.experiment_id)
        state = self._get_or_create_state(session, config)

        # Run just the initial question node
        thread_config = {"configurable": {"thread_id": session_id}}
        result = self.graph.invoke(state, thread_config)

        # Get the initial message
        last_message = result["messages"][-1]
        initial_text = last_message.content

        # Store it
        self.storage.store_message(session_id, "assistant", initial_text)

        return initial_text

    def _get_or_create_state(
        self,
        session: SessionInfo,
        config: Dict[str, Any]
    ) -> ConversationState:
        """Get existing state or create new one"""

        # For simplicity, create a new state
        # In production, would retrieve from checkpointer
        return create_initial_state(
            session_id=session.session_id,
            participant_id=session.participant_id,
            experiment_id=session.experiment_id,
            user_info=session.user_info,
            experiment_config=config
        )

    def export_session(self, session_id: str, format: str = "json") -> Any:
        """
        Export session data.

        Args:
            session_id: Session identifier
            format: Export format (json, csv, etc.)

        Returns:
            Exported data
        """
        return self.storage.export_session(session_id)

    def list_experiments(self) -> list[str]:
        """List available experiments"""
        return self.question_manager.list_experiments()
