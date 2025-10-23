# ESM Chatbot Prompts Guide

This guide shows you where to find and modify all the prompts that control the conversation flow.

## Main Prompt Location

**File:** `core/graph/nodes.py`

This file contains all the conversation logic and prompts for different stages.

---

## Conversation Stages & Their Prompts

### 1. Initial Question (Opening)

**Function:** `initial_question_node()` at line ~29

**What it does:** Starts the conversation with your configured initial question

**Where to customize:**
- The question text itself is in `config/experiments.yaml`:
  ```yaml
  initial_question:
    text: "Your opening question here"
    context: "Optional context/instructions"
  ```

---

### 2. Main Conversation (Follow-up Questions)

**Function:** `conversation_node()` at line ~54

**System Prompt Builder:** `_build_system_prompt()` at line ~123

**What it does:** Generates dynamic follow-up questions based on:
- Research goals from your experiment config
- Topics already covered
- Participant's responses

**Key prompt sections:**

```python
# Line ~145 in nodes.py
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
```

**Where to customize:**
1. **Tone and Style:** In `config/experiments.yaml`:
   ```yaml
   conversation_guidelines:
     tone: "warm, curious, and non-judgmental"
     style: "conversational and natural"
   ```

2. **Research Goals:** In `config/experiments.yaml`:
   ```yaml
   goals:
     - "Goal 1"
     - "Goal 2"
   ```

3. **Conversation Approach:** In `config/experiments.yaml`:
   ```yaml
   conversation_guidelines:
     approach: |
       Your detailed instructions for how the bot should conduct the conversation...
   ```

4. **Follow-up Categories:** In `config/experiments.yaml`:
   ```yaml
   follow_up_categories:
     category_name:
       description: "What to explore"
       example_questions:
         - "Example 1"
         - "Example 2"
   ```

---

### 3. Closing (Ending)

**Function:** `closing_node()` at line ~107

**What it does:** Thanks the participant when the conversation ends

**Current message:**
```python
closing_message = (
    "Thank you so much for sharing about your interaction with me. "
    "Your responses will help us better understand empathy in daily social interactions. "
    "Have a great day!"
)
```

**To customize:** Edit this message directly in `core/graph/nodes.py` at line ~107

Or make it configurable by adding to `config/experiments.yaml`:
```yaml
closing_message: "Your custom thank you message here"
```

---

## Conversation Flow Control

**File:** `core/graph/edges.py`

**Function:** `should_continue_conversation()` at line ~10

**What it controls:** Decides when to end the conversation based on:
- Number of exchanges (default: 8)
- Topics covered vs. goals
- Current conversation stage

**Exit Criteria:** Configured in `config/experiments.yaml`:
```yaml
conversation_guidelines:
  exit_criteria:
    - "Covered all main goal areas"
    - "Participant has shared sufficient detail"
    - "Natural conversation endpoint reached"
    - "8 or more exchanges completed"
```

**To modify:** Edit `core/graph/edges.py` line ~10-50 to change the logic

---

## Quick Customization Checklist

### For a New Study:

1. **Edit `config/experiments.yaml`:**
   - Change experiment name and description
   - Set initial question
   - Define research goals
   - Configure conversation guidelines (tone, style, approach)
   - Add follow-up categories
   - Set exit criteria

2. **Optional - Modify Prompts Directly:**
   - Edit `core/graph/nodes.py` line ~145 for main conversation prompt
   - Edit `core/graph/nodes.py` line ~107 for closing message

3. **Optional - Change Flow Logic:**
   - Edit `core/graph/edges.py` to change when conversation ends
   - Edit `core/graph/nodes.py` line ~193 for topic tracking logic

---

## Adding Conditional Prompts Based on Stage

If you want different prompts at different stages, you can modify `conversation_node()`:

```python
# In core/graph/nodes.py, around line 54

def conversation_node(state: ConversationState) -> Dict[str, Any]:
    exchange_count = state.get("exchange_count", 0)

    # Early stage (first 2 exchanges)
    if exchange_count < 2:
        system_prompt = _build_early_stage_prompt(state)
    # Middle stage (exchanges 3-5)
    elif exchange_count < 5:
        system_prompt = _build_middle_stage_prompt(state)
    # Late stage (exchanges 6+)
    else:
        system_prompt = _build_late_stage_prompt(state)

    # ... rest of the function
```

Then create the new prompt builders for each stage.

---

## Testing Your Prompts

1. Run the Streamlit app: `streamlit run interfaces/streamlit_app.py`
2. Fill out the form
3. Have a conversation
4. Check the exports to see if you're getting the data you need
5. Adjust prompts and retry

---

## Common Adjustments

### Make questions more directive:
Edit line ~145 in `nodes.py`, change:
```python
"Is open-ended when possible"
```
to:
```python
"Asks specific, focused questions about [your topic]"
```

### Add more exchanges:
Edit `config/experiments.yaml`:
```yaml
exit_criteria:
  - "12 or more exchanges completed"  # Change from 8 to 12
```

### Change conversation depth:
Adjust the `approach` in `config/experiments.yaml` to guide the LLM:
```yaml
approach: |
  Focus on getting specific, concrete details rather than general statements.
  Ask follow-up questions about emotions, thoughts, and behaviors.
  Probe for examples when participants make abstract statements.
```

---

## Need Help?

- Most customization happens in `config/experiments.yaml`
- For advanced changes, edit `core/graph/nodes.py`
- For flow control, edit `core/graph/edges.py`
