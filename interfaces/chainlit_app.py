"""
Chainlit UI interface for the ESM Chatbot.

Run with: chainlit run interfaces/chainlit_app.py
"""
import chainlit as cl
from core.api import ESMBot
from config.settings import get_settings
import os

# Initialize settings
settings = get_settings()

# Create bot instance
bot = None


@cl.on_chat_start
async def start():
    """Initialize a new chat session"""
    global bot

    # Initialize bot if not already done
    if bot is None:
        bot = ESMBot()

    # Get available experiments
    experiments = bot.list_experiments()

    if not experiments:
        await cl.Message(
            content="No experiments configured. Please add experiments to config/experiments.yaml"
        ).send()
        return

    # For now, use the first experiment
    # In production, could show a selection UI
    experiment_id = experiments[0]

    # Welcome message with clear instructions
    await cl.Message(
        content=f"""# Welcome to the ESM Chatbot!

You're about to participate in the **{experiment_id.replace('_', ' ').title()}**.

---

## Before We Begin

**📝 Instructions:**
We'll ask you a few questions. Please answer each question using the **chat box at the bottom of the screen**.

After you answer, the next question will appear automatically.

---"""
    ).send()

    # Get user info fields from experiment config
    question_mgr = bot.question_manager
    user_info_fields = question_mgr.get_user_info_fields(experiment_id)

    # Set flag for info collection mode
    cl.user_session.set("collecting_info", True)
    cl.user_session.set("current_field_index", 0)
    cl.user_session.set("user_info_fields", user_info_fields)
    cl.user_session.set("user_info", {})
    cl.user_session.set("experiment_id", experiment_id)
    cl.user_session.set("bot", bot)

    # Ask first question
    if user_info_fields:
        field = user_info_fields[0]
        prompt_text = field.get("prompt", f"Please provide {field.get('name')}")
        is_required = field.get("required", False)

        question_text = f"""### Question 1 of {len(user_info_fields)}

**{prompt_text}**"""

        if is_required:
            question_text += "\n\n🔴 _This field is required_"
        else:
            question_text += "\n\n⚪ _Optional (type 'skip' to skip)_"

        question_text += "\n\n👇 _Please type your answer in the chat box below_"

        await cl.Message(content=question_text).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""

    # Check if we're collecting user info
    collecting_info = cl.user_session.get("collecting_info", False)

    if collecting_info:
        # Handle info collection
        current_index = cl.user_session.get("current_field_index", 0)
        user_info_fields = cl.user_session.get("user_info_fields", [])
        user_info = cl.user_session.get("user_info", {})

        if current_index < len(user_info_fields):
            field = user_info_fields[current_index]
            field_name = field.get("name")
            field_type = field.get("type", "text")
            is_required = field.get("required", False)

            # Get user's answer
            value = message.content.strip()

            # Handle skip
            if value.lower() == 'skip' and not is_required:
                value = None
            elif not value and is_required:
                await cl.Message(content="⚠️ This field is required. Please provide an answer.").send()
                return
            else:
                # Type conversion for numbers
                if field_type == "number" and value:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            await cl.Message(content="⚠️ Please enter a valid number.").send()
                            return

            # Store value
            if value:
                user_info[field_name] = value

            # Move to next field
            current_index += 1
            cl.user_session.set("current_field_index", current_index)
            cl.user_session.set("user_info", user_info)

            # Check if more fields
            if current_index < len(user_info_fields):
                next_field = user_info_fields[current_index]
                prompt_text = next_field.get("prompt", f"Please provide {next_field.get('name')}")
                is_required = next_field.get("required", False)

                question_text = f"""### Question {current_index + 1} of {len(user_info_fields)}

**{prompt_text}**"""

                if is_required:
                    question_text += "\n\n🔴 _This field is required_"
                else:
                    question_text += "\n\n⚪ _Optional (type 'skip' to skip)_"

                question_text += "\n\n👇 _Please type your answer in the chat box below_"

                await cl.Message(content=question_text).send()
            else:
                # All info collected - create session
                experiment_id = cl.user_session.get("experiment_id")
                bot_instance = cl.user_session.get("bot")

                try:
                    participant_id = user_info.get("participant_id", "unknown")
                    session = bot_instance.start_session(
                        participant_id=participant_id,
                        experiment_id=experiment_id,
                        user_info=user_info
                    )

                    # Store session
                    cl.user_session.set("session_id", session.session_id)
                    cl.user_session.set("collecting_info", False)

                    # Transition message
                    await cl.Message(
                        content="✅ Thank you! Your information has been recorded.\n\n---\n\n## Let's Begin\n\nThe study will now start. Please answer the following questions naturally."
                    ).send()

                    # Get initial question
                    initial_msg = bot_instance.get_initial_message(session.session_id)
                    await cl.Message(content=initial_msg).send()

                except ValueError as e:
                    await cl.Message(content=f"❌ Error: {str(e)}").send()
        return

    # Normal conversation mode
    session_id = cl.user_session.get("session_id")
    bot_instance = cl.user_session.get("bot")

    if not session_id or not bot_instance:
        await cl.Message(
            content="⚠️ Session not initialized. Please refresh the page to start again."
        ).send()
        return

    try:
        # Process the message
        result = bot_instance.process_message(
            session_id=session_id,
            message=message.content
        )

        # Send response
        await cl.Message(content=result["response"]).send()

        # If conversation is complete
        if result.get("is_complete", False):
            await cl.Message(
                content="\n\n---\n\n**Session Complete**\n\nThank you for participating! Your session has been saved."
            ).send()

            # Offer export
            actions = [
                cl.Action(
                    name="export",
                    value="export",
                    label="📥 Export Session Data"
                )
            ]
            await cl.Message(
                content="You can export your session data if needed:",
                actions=actions
            ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ An error occurred: {str(e)}"
        ).send()


@cl.action_callback("export")
async def on_export(action: cl.Action):
    """Handle export action"""
    session_id = cl.user_session.get("session_id")
    bot_instance = cl.user_session.get("bot")

    if session_id and bot_instance:
        try:
            # Export session data
            data = bot_instance.export_session(session_id)

            # Save to file
            export_dir = "exports"
            os.makedirs(export_dir, exist_ok=True)
            filename = f"{export_dir}/session_{session_id}.json"

            import json
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

            await cl.Message(
                content=f"Session data exported to: {filename}"
            ).send()

        except Exception as e:
            await cl.Message(
                content=f"Export failed: {str(e)}"
            ).send()


if __name__ == "__main__":
    # This won't run directly, use: chainlit run interfaces/chainlit_app.py
    pass
