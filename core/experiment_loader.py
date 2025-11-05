"""
Experiment loading system for discovering and loading experiments from multiple sources
"""
from typing import Dict, Any, List, Optional
import yaml
import os
import json
from pathlib import Path


class ExperimentLoader:
    """
    Loads experiments from various sources (directories, files, etc.)
    """

    def __init__(self, experiments_dir: Optional[str] = None, load_from_env: bool = True):
        """
        Initialize experiment loader.

        Args:
            experiments_dir: Base directory containing experiments.
                           If None, defaults to 'experiments/' in project root.
            load_from_env: If True, also loads experiments from environment variables.
        """
        if experiments_dir is None:
            # Default to experiments/ directory relative to this file's location
            project_root = Path(__file__).parent.parent
            experiments_dir = project_root / "experiments"

        self.experiments_dir = Path(experiments_dir)
        self.experiments: Dict[str, Dict[str, Any]] = {}
        self._load_all_experiments()

        # Load from environment variables (useful for Streamlit secrets)
        if load_from_env:
            self._load_experiments_from_env()

    def _load_all_experiments(self):
        """
        Discover and load all experiments from the experiments directory.
        Searches in both 'examples/' and 'private/' subdirectories.
        """
        if not self.experiments_dir.exists():
            print(f"Warning: Experiments directory not found: {self.experiments_dir}")
            return

        # Look for experiment files in subdirectories
        search_paths = [
            self.experiments_dir / "examples",
            self.experiments_dir / "private",
            self.experiments_dir,  # Also check root for backward compatibility
        ]

        for search_path in search_paths:
            if search_path.exists() and search_path.is_dir():
                self._load_experiments_from_directory(search_path)

    def _load_experiments_from_directory(self, directory: Path):
        """
        Load all YAML experiment files from a directory.

        Args:
            directory: Directory to search for experiment files
        """
        for yaml_file in directory.glob("*.yaml"):
            try:
                experiment_id = yaml_file.stem  # Filename without extension
                experiment_config = self._load_experiment_file(yaml_file)

                if experiment_config:
                    self.experiments[experiment_id] = experiment_config
                    print(f"Loaded experiment: {experiment_id} from {yaml_file}")

            except Exception as e:
                print(f"Error loading experiment from {yaml_file}: {e}")

    def _load_experiment_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single experiment YAML file.

        Args:
            file_path: Path to the experiment YAML file

        Returns:
            Experiment configuration dictionary
        """
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate using shared validation method
        if self._validate_experiment(config, file_path.stem):
            return config

        return None

    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific experiment.

        Args:
            experiment_id: Experiment identifier (filename without .yaml extension)

        Returns:
            Experiment configuration if found, None otherwise
        """
        return self.experiments.get(experiment_id)

    def list_experiments(self) -> List[str]:
        """
        List all available experiment IDs.

        Returns:
            List of experiment identifiers
        """
        return list(self.experiments.keys())

    def _load_experiments_from_env(self):
        """
        Load experiments from environment variables.

        Supports two formats:
        1. EXPERIMENT_{ID}_YAML: Full YAML content as string
        2. EXPERIMENT_{ID}_JSON: Full experiment config as JSON string

        This is useful for Streamlit Cloud secrets where you can't commit files.

        Example in Streamlit secrets.toml:
        EXPERIMENT_WISE_DECISION_MAKING_YAML = '''
        name: "Study Name"
        description: "..."
        ...
        '''
        """
        # Look for environment variables matching the pattern
        for key, value in os.environ.items():
            # Check for YAML format
            if key.startswith("EXPERIMENT_") and key.endswith("_YAML"):
                # Extract experiment ID from env var name
                # EXPERIMENT_WISE_DECISION_MAKING_YAML -> wise_decision_making
                exp_id = key[11:-5].lower()  # Remove prefix and suffix

                try:
                    experiment_config = yaml.safe_load(value)

                    if self._validate_experiment(experiment_config, exp_id):
                        self.experiments[exp_id] = experiment_config
                        print(f"Loaded experiment: {exp_id} from environment variable {key}")

                except Exception as e:
                    print(f"Error loading experiment from {key}: {e}")

            # Check for JSON format
            elif key.startswith("EXPERIMENT_") and key.endswith("_JSON"):
                exp_id = key[11:-5].lower()

                try:
                    experiment_config = json.loads(value)

                    if self._validate_experiment(experiment_config, exp_id):
                        self.experiments[exp_id] = experiment_config
                        print(f"Loaded experiment: {exp_id} from environment variable {key}")

                except Exception as e:
                    print(f"Error loading experiment from {key}: {e}")

    def _validate_experiment(self, config: Dict[str, Any], exp_id: str) -> bool:
        """
        Validate that experiment config has required fields.

        Args:
            config: Experiment configuration dictionary
            exp_id: Experiment identifier

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(config, dict):
            print(f"Warning: Invalid experiment format for {exp_id}")
            return False

        # Check for essential fields
        required_fields = ['name', 'initial_question', 'goals']
        missing_fields = [field for field in required_fields if field not in config]

        if missing_fields:
            print(f"Warning: Experiment {exp_id} missing required fields: {missing_fields}")
            return False

        return True

    def reload(self):
        """
        Reload all experiments from disk and environment variables.
        Useful for picking up changes without restarting the application.
        """
        self.experiments.clear()
        self._load_all_experiments()
        self._load_experiments_from_env()


def load_legacy_experiments(config_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Load experiments from legacy experiments.yaml format.
    This function provides backward compatibility with the old format.

    Args:
        config_path: Path to the legacy experiments.yaml file

    Returns:
        Dictionary of experiments

    Example legacy format:
        experiments:
          study_name:
            name: "..."
            ...
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config.get("experiments", {})
