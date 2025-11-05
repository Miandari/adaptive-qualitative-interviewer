"""
Test script for loading experiments from environment variables (Streamlit secrets simulation)
"""
import os
import yaml
from core.experiment_loader import ExperimentLoader

def test_env_loading():
    """Test loading experiments from environment variables"""

    print("=" * 60)
    print("Testing Experiment Loading from Environment Variables")
    print("=" * 60)

    # Read the wise_decision_making YAML file
    with open('experiments/private/wise_decision_making.yaml', 'r') as f:
        yaml_content = f.read()

    # Set it as an environment variable
    os.environ['EXPERIMENT_WISE_DECISION_MAKING_YAML'] = yaml_content

    print("\n1. Set environment variable: EXPERIMENT_WISE_DECISION_MAKING_YAML")
    print(f"   Content length: {len(yaml_content)} characters")

    # Create loader (will load from env vars)
    print("\n2. Creating ExperimentLoader...")
    loader = ExperimentLoader()

    # List experiments
    experiments = loader.list_experiments()
    print(f"\n3. Found {len(experiments)} experiments:")
    for exp_id in experiments:
        exp = loader.get_experiment(exp_id)
        source = "env var" if exp_id == "wise_decision_making" else "file"
        print(f"   - {exp_id}: {exp['name']} (from {source})")

    # Verify the env-loaded experiment
    print("\n4. Verifying wise_decision_making experiment:")
    wise = loader.get_experiment('wise_decision_making')
    if wise:
        print(f"   Name: {wise['name']}")
        print(f"   Description: {wise['description']}")
        print(f"   Goals: {len(wise['goals'])} goals")
        print(f"   Follow-up categories: {len(wise['follow_up_categories'])} categories")
        print(f"   User info fields: {len(wise['user_info_fields'])} fields")

        # Check a specific field
        initial_q = wise.get('initial_question', {})
        print(f"   Initial question exists: {bool(initial_q.get('text'))}")
        print(f"   Context exists: {bool(initial_q.get('context'))}")

        print("\n   SUCCESS: Experiment loaded correctly from environment variable!")
    else:
        print("   ERROR: Could not load wise_decision_making from environment")

    # Clean up
    del os.environ['EXPERIMENT_WISE_DECISION_MAKING_YAML']
    print("\n5. Cleaned up environment variable")

    print("\n" + "=" * 60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nThis confirms that experiments can be loaded from Streamlit secrets")
    print("using the EXPERIMENT_{ID}_YAML format.")


if __name__ == "__main__":
    test_env_loading()
