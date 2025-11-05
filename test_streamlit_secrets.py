"""
Test script to verify Streamlit secrets / environment variables
This simulates how Streamlit Cloud loads experiments from secrets
"""
import os
import sys

def test_secret_loading():
    """Test if experiment can be loaded from environment variable"""

    print("=" * 70)
    print("STREAMLIT SECRETS SIMULATION TEST")
    print("=" * 70)

    # Check if the environment variable exists
    secret_name = "EXPERIMENT_WISE_DECISION_MAKING_YAML"

    print(f"\n1. Checking for environment variable: {secret_name}")

    if secret_name in os.environ:
        content = os.environ[secret_name]
        print(f"   ✓ Found! Length: {len(content)} characters")

        # Try to parse as YAML
        try:
            import yaml
            parsed = yaml.safe_load(content)

            print(f"\n2. YAML Parsing:")
            print(f"   ✓ Valid YAML structure")
            print(f"   ✓ Name: {parsed.get('name', 'MISSING')}")
            print(f"   ✓ Version: {parsed.get('version', 'MISSING')}")
            print(f"   ✓ Goals: {len(parsed.get('goals', []))} goals")
            print(f"   ✓ Categories: {len(parsed.get('follow_up_categories', {}))} categories")

            # Check required fields
            print(f"\n3. Required Fields:")
            required = ['name', 'initial_question', 'goals']
            for field in required:
                if field in parsed:
                    print(f"   ✓ {field}: present")
                else:
                    print(f"   ✗ {field}: MISSING!")

            print(f"\n4. Test Result: SUCCESS!")
            print(f"   The secret would be loaded correctly by ExperimentLoader")

        except Exception as e:
            print(f"\n2. YAML Parsing:")
            print(f"   ✗ ERROR: {e}")
            print(f"\n   This is why the experiment isn't loading!")
            print(f"   Check your YAML formatting in Streamlit secrets")

    else:
        print(f"   ✗ Not found!")
        print(f"\n   This means:")
        print(f"   - In Streamlit Cloud: The secret isn't set or named incorrectly")
        print(f"   - Locally: You need to set it for testing")

    print("\n" + "=" * 70)
    print("HOW TO FIX:")
    print("=" * 70)
    print("""
In Streamlit Cloud Secrets, make sure you have:

EXPERIMENT_WISE_DECISION_MAKING_YAML = '''
# Wise Decision-Making Process Study
# Version: 2.0
...your full YAML content...
'''

Key points:
1. Variable name must be EXACTLY: EXPERIMENT_WISE_DECISION_MAKING_YAML
2. Use triple single quotes: '''
3. Paste the ENTIRE yaml file
4. No extra spaces before/after the content
5. Save and wait for app to restart
    """)


def test_experiment_loader():
    """Test if ExperimentLoader would pick it up"""
    print("\n" + "=" * 70)
    print("TESTING WITH EXPERIMENTLOADER")
    print("=" * 70)

    try:
        from core.experiment_loader import ExperimentLoader

        loader = ExperimentLoader()
        experiments = loader.list_experiments()

        print(f"\nLoaded experiments: {len(experiments)}")
        for exp_id in experiments:
            exp = loader.get_experiment(exp_id)
            source = "(from env var)" if exp_id == "wise_decision_making" and "EXPERIMENT_WISE_DECISION_MAKING_YAML" in os.environ else "(from file)"
            print(f"  - {exp_id}: {exp['name']} {source}")

        if "wise_decision_making" in experiments:
            print(f"\n✓ SUCCESS: wise_decision_making is available!")
        else:
            print(f"\n✗ PROBLEM: wise_decision_making not found!")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_secret_loading()
    test_experiment_loader()
