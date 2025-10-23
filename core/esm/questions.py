"""
Question management for ESM conversations
"""
from typing import Dict, Any, List, Optional
import yaml


class QuestionManager:
    """
    Manages questions and conversation flow for ESM studies.
    """

    def __init__(self, config_path: str):
        """
        Initialize with experiment configuration file.

        Args:
            config_path: Path to the experiment YAML configuration
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        self.experiments = config.get("experiments", {})

    def get_experiment_config(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Experiment configuration if found, None otherwise
        """
        return self.experiments.get(experiment_id)

    def get_user_info_fields(self, experiment_id: str) -> List[Dict[str, Any]]:
        """
        Get required user information fields for an experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            List of user info field configurations
        """
        config = self.get_experiment_config(experiment_id)
        if config:
            return config.get("user_info_fields", [])
        return []

    def validate_user_info(
        self,
        experiment_id: str,
        user_info: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """
        Validate that required user info fields are provided.

        Args:
            experiment_id: Experiment identifier
            user_info: User information to validate

        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        fields = self.get_user_info_fields(experiment_id)
        missing = []

        for field in fields:
            field_name = field.get("name")
            is_required = field.get("required", False)

            if is_required and field_name not in user_info:
                missing.append(field_name)

        return len(missing) == 0, missing

    def get_initial_question(self, experiment_id: str) -> Optional[Dict[str, str]]:
        """
        Get the initial probe question for an experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Initial question configuration
        """
        config = self.get_experiment_config(experiment_id)
        if config:
            return config.get("initial_question")
        return None

    def get_follow_up_categories(self, experiment_id: str) -> Dict[str, Any]:
        """
        Get follow-up question categories for an experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Dictionary of follow-up categories
        """
        config = self.get_experiment_config(experiment_id)
        if config:
            return config.get("follow_up_categories", {})
        return {}

    def get_conversation_guidelines(self, experiment_id: str) -> Dict[str, Any]:
        """
        Get conversation guidelines for an experiment.

        Args:
            experiment_id: Experiment identifier

        Returns:
            Conversation guidelines dictionary
        """
        config = self.get_experiment_config(experiment_id)
        if config:
            return config.get("conversation_guidelines", {})
        return {}

    def list_experiments(self) -> List[str]:
        """
        List all available experiment IDs.

        Returns:
            List of experiment identifiers
        """
        return list(self.experiments.keys())
