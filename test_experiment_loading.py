"""
Test script for the new experiment loading system
"""
from core.experiment_loader import ExperimentLoader
from core.esm.questions import QuestionManager

def test_experiment_loader():
    """Test the ExperimentLoader directly"""
    print("=" * 60)
    print("Testing ExperimentLoader")
    print("=" * 60)

    loader = ExperimentLoader()

    print(f"\nFound {len(loader.experiments)} experiments:")
    for exp_id in loader.list_experiments():
        exp = loader.get_experiment(exp_id)
        print(f"  - {exp_id}: {exp['name']}")

    print("\nTesting specific experiment retrieval:")
    empathy = loader.get_experiment("empathy_study")
    if empathy:
        print(f"  Empathy Study: {empathy['name']}")
        print(f"  Goals: {len(empathy.get('goals', []))} goals")
        print(f"  Categories: {len(empathy.get('follow_up_categories', {}))} categories")
    else:
        print("  ERROR: Could not load empathy_study")

    wise = loader.get_experiment("wise_decision_making")
    if wise:
        print(f"  Wise Decision Making: {wise['name']}")
        print(f"  Goals: {len(wise.get('goals', []))} goals")
        print(f"  Categories: {len(wise.get('follow_up_categories', {}))} categories")
    else:
        print("  ERROR: Could not load wise_decision_making")

    return loader.experiments


def test_question_manager():
    """Test the QuestionManager with new loading system"""
    print("\n" + "=" * 60)
    print("Testing QuestionManager (New Mode)")
    print("=" * 60)

    # Test new mode (directory loading)
    qm = QuestionManager()

    experiments = qm.list_experiments()
    print(f"\nFound {len(experiments)} experiments via QuestionManager:")
    for exp_id in experiments:
        print(f"  - {exp_id}")

    print("\nTesting experiment methods:")
    for exp_id in experiments:
        config = qm.get_experiment_config(exp_id)
        if config:
            print(f"\n  {exp_id}:")
            print(f"    Name: {config.get('name')}")
            print(f"    User info fields: {len(qm.get_user_info_fields(exp_id))}")

            initial_q = qm.get_initial_question(exp_id)
            if initial_q:
                print(f"    Initial question: {initial_q['text'][:50]}...")

            guidelines = qm.get_conversation_guidelines(exp_id)
            print(f"    Tone: {guidelines.get('tone', 'N/A')}")


def test_legacy_mode():
    """Test backward compatibility with legacy experiments.yaml"""
    print("\n" + "=" * 60)
    print("Testing Legacy Mode (experiments.yaml)")
    print("=" * 60)

    import os
    legacy_path = "config/experiments.yaml"

    if os.path.exists(legacy_path):
        print(f"\nLegacy file exists: {legacy_path}")
        qm_legacy = QuestionManager(config_path=legacy_path)

        experiments = qm_legacy.list_experiments()
        print(f"Found {len(experiments)} experiments in legacy mode:")
        for exp_id in experiments:
            print(f"  - {exp_id}")
    else:
        print(f"\nLegacy file not found: {legacy_path}")
        print("This is expected if you've migrated to the new system.")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("EXPERIMENT LOADING SYSTEM TEST")
    print("=" * 60)

    try:
        # Test 1: ExperimentLoader
        experiments = test_experiment_loader()

        # Test 2: QuestionManager (new mode)
        test_question_manager()

        # Test 3: Legacy mode
        test_legacy_mode()

        print("\n" + "=" * 60)
        print("TESTS COMPLETED")
        print("=" * 60)

        if len(experiments) > 0:
            print("\nSUCCESS: All experiments loaded successfully!")
        else:
            print("\nWARNING: No experiments were loaded.")

    except Exception as e:
        print(f"\nERROR during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
