# Streamlit Cloud Deployment with Private Experiments

This guide explains how to deploy AI Experimenter to Streamlit Cloud while keeping your proprietary experiment prompts private using Streamlit secrets.

## Overview

The system supports loading experiments from three sources:
1. **Public experiments** - Committed to `experiments/examples/` (visible in GitHub)
2. **Local private experiments** - In `experiments/private/` (gitignored, local only)
3. **Secrets-based experiments** - Loaded from environment variables (for cloud deployment)

## Quick Start: Deploying with Private Experiments

### Step 1: Deploy to Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `interfaces/streamlit_app.py`
6. Click "Deploy"

### Step 2: Add Your API Keys

1. In Streamlit Cloud dashboard, click your app
2. Click "Settings" (gear icon, bottom right)
3. Go to "Secrets" tab
4. Add your LLM API keys:

```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-your-actual-key-here"
LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-4o"

# OR Anthropic Configuration
# ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
# LLM_PROVIDER = "anthropic"
# LLM_MODEL = "claude-3-5-sonnet-20241022"
```

5. Click "Save"

At this point, your app will work with the public `empathy_study` experiment.

### Step 3: Add Private Experiments (Optional)

To add your private experiments to Streamlit Cloud:

1. Copy your complete experiment YAML from `experiments/private/wise_decision_making.yaml`
2. In Streamlit Cloud secrets, add:

```toml
EXPERIMENT_WISE_DECISION_MAKING_YAML = '''
name: "Wise Decision-Making Process Study"
description: "Exploring how people think through complex decisions with competing values and uncertainty"

user_info_fields:
  - name: "participant_id"
    type: "text"
    required: true
    prompt: "Please enter your Participant ID"
  - name: "age"
    type: "number"
    required: false
    prompt: "What is your age?"
  - name: "conversation_depth"
    type: "select"
    required: false
    prompt: "Preferred conversation depth"
    options:
      - "Short (5 exchanges)"
      - "Medium (8 exchanges)"
      - "Deep (12+ exchanges)"

initial_question:
  text: "Put yourself in the position of the main character in this situation. Please describe how you personally would proceed here. How would you approach making this decision?"
  context: |
    Thank you for participating in our study on decision-making processes.

    As you read this story, consider it happening to you:

    **Employment Decision Scenario**

    You work at a small company where the job is stable, and your coworkers are friendly. The pay, however, barely covers your expenses, and lately you've been feeling growing pressure from your family to find something better. Recently, a recruiter from a large firm reached out to say that your experience could make you a strong candidate for a higher-paying position. However, to apply, you need to complete several months of a trial period that requires leaving your current job. It would mean quitting your stable role, spending months preparing, and not knowing if you will be hired at the end. Staying would keep you financially afloat, but feeling stuck; leaving could open new opportunities but also bring uncertainty and risk.

goals:
  - "Understand their decision-making process and reasoning steps"
  - "Explore how they identify and gather relevant information"
  - "Examine how they weigh competing values and priorities"
  - "Assess how they evaluate and manage uncertainty and risk"
  - "Identify their emotional awareness and regulation strategies"

follow_up_categories:
  information_gathering:
    description: "Explore how they identify what information they need and seek it out"
    example_questions:
      - "You mentioned gathering information. What specific information would you need to make this decision?"
      - "How would you go about getting that information?"
      - "How would you know when you have enough information to decide?"

  value_prioritization:
    description: "Understand how they weigh competing values (security vs growth, family vs personal fulfillment)"
    example_questions:
      - "I notice you're weighing [X vs Y]. How do you decide which matters more to you?"
      - "What makes [value] particularly important to you in this situation?"
      - "How do your family's expectations factor into your thinking?"

  risk_assessment:
    description: "Examine how they evaluate uncertainty and potential outcomes"
    example_questions:
      - "You mentioned the risk of [X]. How do you evaluate whether that risk is worth taking?"
      - "What would make you more comfortable with that uncertainty?"
      - "How do you think about the potential downsides versus upsides?"

  emotional_regulation:
    description: "Understand how they manage emotions during the decision process"
    example_questions:
      - "You mentioned feeling [emotion]. How does that influence your thinking about this decision?"
      - "How would you manage [pressure/fear/excitement] while making this choice?"
      - "What helps you think clearly when facing difficult decisions?"

  process_reflection:
    description: "Encourage metacognitive reflection on their approach"
    example_questions:
      - "Looking at how you've thought through this, what's guiding your approach?"
      - "Is this how you typically make important decisions?"
      - "What might you be overlooking in your process?"

conversation_guidelines:
  tone: "curious and thoughtful, like a researcher genuinely interested in understanding"
  style: "conversational and exploratory, focused on process over outcome"
  probing_approach: "gentle"
  approach: |
    Your goal is to understand HOW this person thinks through complex decisions, not to judge their choice or push them toward a particular outcome.

    **Core Principles:**
    1. Focus on PROCESS over outcome - care about their reasoning, not their final decision
    2. Listen for natural mentions of the 4 key aspects (info gathering, values, risk, emotions)
    3. Follow up dynamically based on what THEY bring up
    4. Use gentle probing to explore deeper, not to challenge
    5. Ask "how" and "why" questions to unpack their reasoning

    Ask ONE question at a time. Keep questions open-ended. Show genuine curiosity about their unique process.
    Aim for depth based on user preference: 5 exchanges (short), 8 exchanges (medium), or 12+ exchanges (deep).

  exit_criteria:
    - "Explored their decision-making process across multiple dimensions"
    - "Participant has reflected on their approach with sufficient depth"
    - "Natural conversation endpoint reached"
    - "Target exchange count reached based on depth setting"
    - "Covered at least 3 of the 4 key process aspects"
'''
```

3. Click "Save"
4. Your app will automatically restart with both experiments available

## Environment Variable Format

**Pattern:** `EXPERIMENT_{ID}_YAML`

- `{ID}` must be UPPERCASE with UNDERSCORES
- The experiment will be accessible using the lowercase version with underscores
- Example: `EXPERIMENT_WISE_DECISION_MAKING_YAML` → accessible as `wise_decision_making`

**Supported Formats:**
- `EXPERIMENT_{ID}_YAML` - YAML string (recommended)
- `EXPERIMENT_{ID}_JSON` - JSON string (alternative)

## Local Development with Secrets

To test locally with secrets:

1. Copy the example file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml` with your actual values

3. The `.streamlit/secrets.toml` file is gitignored, so it stays private

4. Run Streamlit locally:
   ```bash
   streamlit run interfaces/streamlit_app.py
   ```

## Adding Multiple Private Experiments

You can add as many private experiments as needed:

```toml
# First experiment
EXPERIMENT_WISE_DECISION_MAKING_YAML = '''
# ... content ...
'''

# Second experiment
EXPERIMENT_MY_OTHER_STUDY_YAML = '''
# ... content ...
'''

# Third experiment
EXPERIMENT_ANOTHER_EXPERIMENT_YAML = '''
# ... content ...
'''
```

## Troubleshooting

### Experiment Not Loading

**Check that:**
1. Variable name follows the pattern `EXPERIMENT_{ID}_YAML`
2. YAML is properly formatted (indentation uses spaces, not tabs)
3. Triple quotes `'''` are used correctly
4. Required fields are present: `name`, `initial_question`, `goals`
5. App has been restarted after adding secrets

### YAML Formatting Issues

**Common issues:**
- Indentation must use spaces (2 spaces per level)
- Multi-line strings use `|` operator
- Lists start with `-` followed by a space
- Nested objects require proper indentation

**Example of correct formatting:**
```yaml
initial_question:
  text: "Your question"
  context: |
    Line 1
    Line 2

goals:
  - "Goal 1"
  - "Goal 2"

follow_up_categories:
  category_name:
    description: "Description"
    example_questions:
      - "Question 1"
      - "Question 2"
```

### Viewing Logs

In Streamlit Cloud:
1. Click "Manage app" (three dots)
2. Click "Logs"
3. Look for messages like:
   - `Loaded experiment: wise_decision_making from environment variable EXPERIMENT_WISE_DECISION_MAKING_YAML`
   - Or error messages about missing fields or YAML parsing

## Security Best Practices

1. **Never commit secrets.toml** - It's already in `.gitignore`
2. **Use Streamlit Cloud secrets** - Don't hardcode sensitive data
3. **Rotate API keys regularly** - Especially if shared
4. **Limit experiment access** - Only add experiments you want public users to access

## Benefits of This Approach

- **Privacy**: Proprietary prompts never touch GitHub
- **Flexibility**: Different experiments for dev/staging/production
- **Security**: Secrets managed by Streamlit Cloud
- **Simplicity**: No separate database or file storage needed
- **Version Control**: Still track public experiments in git

## Next Steps

- Add more private experiments as needed
- Update experiment content by editing secrets (no redeployment needed)
- Consider adding experiment-level access control (future enhancement)
- Export data for analysis using the built-in export functionality

## Questions?

See also:
- `experiments/README.md` - How to create experiments
- `claude.md` - Development roadmap and architecture
- `.streamlit/secrets.toml.example` - Complete secrets template
