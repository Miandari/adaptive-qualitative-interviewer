"""
Streamlit UI interface for the ESM Chatbot.

Run with: streamlit run interfaces/streamlit_app.py
"""
import sys
from pathlib import Path

# Add project root to Python path for Streamlit Cloud deployment
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from core.api import ESMBot
from config.settings import get_settings
import json
import os

# Initialize settings
settings = get_settings()

# Page config
st.set_page_config(
    page_title="ESM Chatbot",
    layout="centered"
)

# Check for API keys before initializing
def check_api_keys():
    """Check if API keys are configured"""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not openai_key and not anthropic_key:
        st.error("⚠️ **API Key Not Configured**")
        st.markdown("""
        Please configure your API key in Streamlit Cloud:

        1. Click **"Manage app"** (bottom right)
        2. Click **"Settings"** → **"Secrets"**
        3. Add your API key:

        ```toml
        OPENAI_API_KEY = "sk-your-key-here"
        LLM_PROVIDER = "openai"
        LLM_MODEL = "gpt-4o"
        ```

        Or for Anthropic:

        ```toml
        ANTHROPIC_API_KEY = "sk-ant-your-key-here"
        LLM_PROVIDER = "anthropic"
        LLM_MODEL = "claude-3-5-sonnet-20241022"
        ```

        4. Click **"Save"** and the app will restart
        """)
        st.stop()

# Initialize bot
@st.cache_resource
def get_bot():
    return ESMBot()

# Check API keys first
check_api_keys()
bot = get_bot()

# Initialize session state
if "session_started" not in st.session_state:
    st.session_state.session_started = False
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.conversation_complete = False
    st.session_state.selected_experiment = None

# Get experiments
experiments = bot.list_experiments()

if not experiments:
    st.error("No experiments configured. Please add experiments to the experiments/ directory")
    st.stop()

# STEP 1: Info Collection Screen
if not st.session_state.session_started:
    st.title("Adaptive Qualitative Interviewer")

    # Experiment selection
    if len(experiments) > 1 and st.session_state.selected_experiment is None:
        st.markdown("### Select Study")

        for exp_id in experiments:
            exp_config = bot.question_manager.get_experiment_config(exp_id)
            exp_name = exp_config.get("name", exp_id)
            exp_desc = exp_config.get("description", "")

            if st.button(f"**{exp_name}**\n\n{exp_desc}", key=f"select_{exp_id}", use_container_width=True):
                st.session_state.selected_experiment = exp_id
                st.rerun()
        st.stop()

    # Use selected experiment or default to first one
    experiment_id = st.session_state.selected_experiment or experiments[0]
    exp_config = bot.question_manager.get_experiment_config(experiment_id)

    st.subheader(f"Welcome to the {exp_config.get('name', experiment_id)}")

    st.markdown("---")

    st.markdown("### Participant Information")
    st.markdown("Please fill out the form below to begin the study.")

    # Get user info fields
    user_info_fields = bot.question_manager.get_user_info_fields(experiment_id)

    # Create form
    with st.form("user_info_form"):
        user_info = {}

        for field in user_info_fields:
            field_name = field.get("name")
            field_type = field.get("type", "text")
            is_required = field.get("required", False)
            prompt_text = field.get("prompt", f"Please provide {field_name}")

            # Add label with required indicator
            label = prompt_text
            if is_required:
                label += " *"

            # Create appropriate input based on field type
            if field_type == "number":
                value = st.number_input(
                    label,
                    min_value=0,
                    step=1,
                    key=field_name
                )
                if value or not is_required:
                    user_info[field_name] = value
            elif field_type == "select":
                # For multiple choice
                options = field.get("options", [])
                value = st.selectbox(
                    label,
                    options=[""] + options if not is_required else options,
                    key=field_name
                )
                if value:
                    user_info[field_name] = value
            else:
                # Text input
                value = st.text_input(
                    label,
                    key=field_name
                )
                if value:
                    user_info[field_name] = value

        st.markdown("_* Required fields_")

        # Submit button
        submitted = st.form_submit_button("Start Study", use_container_width=True, type="primary")

        if submitted:
            # Validate required fields
            is_valid, missing = bot.question_manager.validate_user_info(
                experiment_id,
                user_info
            )

            if not is_valid:
                st.error(f"Please fill in required fields: {', '.join(missing)}")
            else:
                # Create session
                try:
                    participant_id = user_info.get("participant_id", "unknown")
                    session = bot.start_session(
                        participant_id=participant_id,
                        experiment_id=experiment_id,
                        user_info=user_info
                    )

                    # Store in session state
                    st.session_state.session_id = session.session_id
                    st.session_state.session_started = True

                    # Get initial message
                    initial_msg = bot.get_initial_message(session.session_id)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": initial_msg
                    })

                    # Rerun to show chat
                    st.rerun()

                except ValueError as e:
                    st.error(f"Error: {str(e)}")

# STEP 2: Chat Interface
else:
    # Get experiment name for title
    exp_id = st.session_state.get("selected_experiment", experiments[0])
    exp_config = bot.question_manager.get_experiment_config(exp_id)
    st.title(exp_config.get("name", "Study Conversation"))

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input (only if conversation not complete)
    if not st.session_state.conversation_complete:
        if prompt := st.chat_input("Type your response here..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get bot response
            try:
                result = bot.process_message(
                    session_id=st.session_state.session_id,
                    message=prompt
                )

                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"]
                })

                # Check if complete
                if result.get("is_complete", False):
                    st.session_state.conversation_complete = True

                # Rerun to show new message
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        # Conversation complete
        st.success("Session Complete! Thank you for participating.")

        # Export button
        if st.button("Export Session Data", use_container_width=True):
            data = bot.export_session(st.session_state.session_id)

            # Save to file
            os.makedirs("exports", exist_ok=True)
            filename = f"exports/session_{st.session_state.session_id}.json"

            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

            st.success(f"Data exported to: {filename}")

            # Also provide download button
            st.download_button(
                label="Download Session Data",
                data=json.dumps(data, indent=2),
                file_name=f"session_{st.session_state.session_id}.json",
                mime="application/json"
            )

        # Option to start new session
        if st.button("Start New Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()
