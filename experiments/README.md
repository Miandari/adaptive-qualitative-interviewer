# Experiments Directory

This directory contains experiment definitions for the AI Experimenter framework. Experiments define the research questions, conversation flow, and data collection parameters for qualitative research interviews conducted via AI.

## Directory Structure

```
experiments/
├── examples/           # Public example experiments (included in repository)
│   └── empathy_study.yaml
├── private/            # Your private experiments (gitignored)
│   └── wise_decision_making.yaml
└── README.md          # This file
```

## How Experiments Are Loaded

The system automatically discovers and loads all `.yaml` files from:
1. `experiments/examples/` - Public example experiments
2. `experiments/private/` - Your private experiments (not tracked in git)

Each experiment file should be named with a unique identifier (e.g., `my_study.yaml`). This identifier will be used to reference the experiment throughout the system.

## Creating a New Experiment

### Basic Structure

Create a new `.yaml` file in either `examples/` (for public experiments) or `private/` (for private experiments):

```yaml
# Study Title and Description
name: "Your Study Name"
description: "Brief description of your research"

# User information fields (collected at session start)
user_info_fields:
  - name: "participant_id"
    type: "text"
    required: true
    prompt: "Please enter your Participant ID"
  - name: "age"
    type: "number"
    required: false
    prompt: "What is your age?"

# Initial question presented to participants
initial_question:
  text: "Your opening question here"
  context: |
    Background information or scenario description.
    Can be multiple paragraphs.

# Research goals (guides conversation direction)
goals:
  - "First research objective"
  - "Second research objective"
  - "Third research objective"

# Follow-up question categories
follow_up_categories:
  category_name:
    description: "What this category explores"
    example_questions:
      - "Example question 1"
      - "Example question 2"
      - "Example question 3"

# Conversation guidelines for the AI interviewer
conversation_guidelines:
  tone: "warm, curious, and non-judgmental"
  style: "conversational and natural"
  approach: |
    Instructions for how the AI should conduct the interview.

    Include:
    - How to follow up on responses
    - What to probe deeper on
    - How many exchanges to aim for

  exit_criteria:
    - "When to end the conversation"
    - "Goal completion requirements"
```

## Field Descriptions

### Required Top-Level Fields

- **name**: Display name for your experiment
- **description**: Brief description of the research purpose
- **initial_question**: The opening question and context
- **goals**: List of research objectives
- **conversation_guidelines**: Instructions for the AI interviewer

### User Info Fields

Collect demographic or identification data at the start of each session:

```yaml
user_info_fields:
  - name: "field_name"        # Internal identifier
    type: "text"              # Options: text, number, select
    required: true            # Whether field is mandatory
    prompt: "Question text"   # What to ask the participant
    options:                  # (Only for type: select)
      - "Option 1"
      - "Option 2"
```

**Supported field types:**
- `text`: Free-form text input
- `number`: Numeric input
- `select`: Dropdown selection (requires `options` list)

### Initial Question

The first question presented to participants:

```yaml
initial_question:
  text: "The actual question"
  context: "Background, scenario, or framing information"
```

### Goals

Research objectives that guide the conversation. The AI will attempt to cover these areas:

```yaml
goals:
  - "Understand X"
  - "Explore Y"
  - "Assess Z"
```

### Follow-up Categories

Organize potential follow-up questions by theme. The AI uses these as inspiration:

```yaml
follow_up_categories:
  category_identifier:
    description: "Brief description of this category's purpose"
    example_questions:
      - "Example question 1"
      - "Example question 2"
```

### Conversation Guidelines

Instructions for how the AI should conduct the interview:

```yaml
conversation_guidelines:
  tone: "Desired conversational tone"
  style: "Interaction style"
  probing_approach: "gentle"  # Optional: how to probe deeper

  approach: |
    Detailed instructions on:
    - How to follow up on responses
    - What to probe deeper on
    - How to transition between topics
    - Target number of exchanges

  exit_criteria:
    - "Condition 1 for ending"
    - "Condition 2 for ending"
```

## Examples

See the files in `examples/` for complete working examples:

### Empathy Study Example
`examples/empathy_study.yaml` - Explores daily empathy in social interactions

Key features:
- Collects context about recent interactions
- Explores perspective-taking and emotional awareness
- Targets 5-8 exchanges

### Decision Making Study Example
`examples/wise_decision_making.yaml` - Examines decision-making processes

Key features:
- Presents a scenario with competing values
- Explores information gathering and risk assessment
- Allows depth customization (5, 8, or 12+ exchanges)

## Best Practices

### 1. Clear Research Goals
Define specific, measurable research objectives. The AI will use these to guide the conversation.

### 2. Open-Ended Questions
Frame questions to encourage elaboration rather than yes/no answers.

### 3. Example Questions
Provide diverse example questions in each category. The AI uses these as inspiration but doesn't ask them verbatim.

### 4. Conversational Tone
Write guidelines in a natural, conversational style. The AI will mirror this tone.

### 5. Exit Criteria
Be specific about when the conversation should end (e.g., number of exchanges, goal coverage).

### 6. Test Your Experiment
Always test with a few trial participants before collecting real data.

## Privacy and Sharing

### Private Experiments
- Store in `experiments/private/`
- Automatically gitignored
- Not included when sharing repository

### Public Examples
- Store in `experiments/examples/`
- Included in repository
- Sanitize any proprietary content

### Naming Conventions
- Use descriptive filenames: `empathy_study.yaml`, not `exp1.yaml`
- Use snake_case for filenames
- Avoid spaces in filenames

## Troubleshooting

### Experiment Not Loading

**Check that:**
1. File is in `examples/` or `private/` directory
2. File has `.yaml` extension
3. Required fields are present (name, initial_question, goals)
4. YAML syntax is valid (use a YAML validator)

### YAML Syntax Errors

Common issues:
- Indentation must use spaces (not tabs)
- Strings with special characters need quotes
- Multi-line text uses `|` or `>` operators

**Example of proper multi-line text:**
```yaml
context: |
  First paragraph here.

  Second paragraph here.
```

### Missing Required Fields

The system requires these fields:
- `name`
- `initial_question` (with `text` and `context`)
- `goals` (list with at least one item)

## Advanced Features (Coming Soon)

Future versions will support:
- Custom conversation stages beyond the default 3-stage flow
- Conditional branching logic
- Custom evaluation functions
- Plugin system for extending functionality

## Getting Help

- Check example experiments in `examples/` directory
- Review the main project documentation
- See `claude.md` for development roadmap and architecture

## Quick Start Checklist

- [ ] Create new `.yaml` file in appropriate directory
- [ ] Add required fields (name, initial_question, goals)
- [ ] Define user info fields for demographics
- [ ] Write follow-up categories with example questions
- [ ] Set conversation guidelines (tone, style, approach)
- [ ] Define exit criteria
- [ ] Test with trial participants
- [ ] Iterate based on feedback
