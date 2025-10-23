# Wise Decision-Making Study Guide

## Overview

The **Wise Decision-Making Process Study** is configured to explore how people think through complex decisions with competing values and uncertainty. Unlike traditional surveys that ask about final decisions, this study focuses on understanding the **PROCESS** of decision-making.

## Key Features

### 1. Employment Scenario
Participants are presented with a realistic employment dilemma involving:
- **Stability vs. Opportunity** trade-off
- **Family pressure** vs. personal contentment
- **Known security** vs. unknown potential
- **Financial safety** vs. growth

### 2. Process-Focused Investigation

The conversation explores **4 key aspects** of decision-making:

#### A. Information Gathering
- What information do they need?
- How would they get it?
- When is enough information "enough"?

#### B. Value Prioritization
- How do they weigh competing values (security vs growth)?
- What makes certain values more important?
- How do family expectations factor in?

#### C. Risk Assessment
- How do they evaluate uncertainty?
- What's their risk tolerance?
- How do they think about potential outcomes?

#### D. Emotional Regulation
- How do emotions influence their thinking?
- How do they manage pressure/fear/excitement?
- How do they balance emotion vs logic?

### 3. Dynamic Follow-Ups

The bot **listens** for which aspects the participant naturally mentions, then explores those areas deeper through:
- "How" and "why" questions
- Process probing ("Walk me through your thinking...")
- Gentle clarification ("I'm curious - have you considered...")

### 4. Configurable Depth

Participants can choose conversation depth:
- **Short**: 5 exchanges
- **Medium**: 8 exchanges
- **Deep**: 12+ exchanges

## How to Use

### Running the Study

1. **Start the application:**
```bash
streamlit run interfaces/streamlit_app.py
```

2. **Select the study:**
   - You'll see experiment options
   - Click "Wise Decision-Making Process Study"

3. **Fill participant info:**
   - Participant ID (required)
   - Age (optional)
   - Conversation depth preference (optional)

4. **Scenario is presented:**
   - Participant reads the employment scenario
   - Initial question appears asking how they'd approach it

5. **Conversation unfolds:**
   - Bot asks ONE question at a time
   - Follows up based on what participant mentions
   - Explores their process dynamically
   - No judgment, just curiosity

6. **Conversation ends when:**
   - Target exchange count reached (based on depth)
   - Covered at least 3 of 4 process aspects
   - Natural endpoint reached

## Conversation Flow Example

**Bot:** "Put yourself in this situation. How would you approach making this decision?"

**Participant:** "I'd start by gathering more information about the trial period and what it involves..."

**Bot:** "You mentioned gathering information. What specific information would you need to make this decision?"

**Participant:** "I'd want to know success rates, what happens if I fail, and whether I can return to my old job..."

**Bot:** "That's interesting. How would you go about getting that information?"

*[Continues exploring their information-gathering process]*

**Bot:** "You've mentioned both financial security and growth opportunities. How do you decide which matters more to you?"

*[Transitions to exploring value prioritization]*

## Prompts Location

All prompts are configured in: `config/experiments.yaml`

Under the `wise_decision_making` section:

- **Scenario text**: `initial_question.context`
- **Opening question**: `initial_question.text`
- **Follow-up categories**: `follow_up_categories` (5 categories with example questions)
- **Conversation guidelines**: `conversation_guidelines.approach`
- **Exit criteria**: `conversation_guidelines.exit_criteria`

## Customizing the Study

### Change the Scenario

Edit `config/experiments.yaml` line 123-130:

```yaml
initial_question:
  context: |
    Your new scenario here...
```

### Adjust Conversation Depth

Edit line 116 to change depth options:

```yaml
options:
  - "Short (5 exchanges)"
  - "Medium (8 exchanges)"
  - "Deep (15 exchanges)"  # Changed to 15
```

Then update `core/graph/edges.py` line 47 to handle new depth.

### Add New Follow-Up Categories

In `config/experiments.yaml`, add new category under `follow_up_categories`:

```yaml
new_category_name:
  description: "What this explores"
  example_questions:
    - "Question 1"
    - "Question 2"
```

### Modify Probing Style

Edit `conversation_guidelines.approach` (line 193) to adjust:
- How directive vs exploratory questions are
- Level of challenge vs support
- Depth of metacognitive reflection

## Data Export

After each session, you can export:
- Full conversation transcript
- Participant responses
- Exchange count and topics covered
- Session metadata

Export formats: JSON, CSV

## Research Considerations

### What This Captures

✅ **Process insights:**
- Order of considerations
- Natural vs prompted topics
- Depth of reflection
- Metacognitive awareness

✅ **Individual differences:**
- Information-seeking behavior
- Value hierarchies
- Risk tolerance
- Emotional awareness

### What This Doesn't Capture

❌ Final decision outcome (not the focus)
❌ Demographic predictors (unless you add them)
❌ Real-world behavior (hypothetical scenario)

## Tips for Analysis

1. **Code for process aspects**: Tag which of the 4 aspects participants naturally mention
2. **Track order**: Does information gathering come before value prioritization?
3. **Depth indicators**: Look for metacognitive statements ("I usually...", "I tend to...")
4. **Emotional awareness**: Note when participants acknowledge emotions vs ignore them
5. **Complexity**: Count number of factors considered

## Next Steps

### Adding More Scenarios

You can add multiple scenarios to the same study:

1. Create scenario variations in the config
2. Randomize which scenario is shown
3. Or ask all participants about multiple scenarios

### Adding Follow-Up Questions

After the main conversation, you can add:
- "Have you faced a similar situation?"
- "What happened when you did?"
- Background check questions

Just add to the `goals` and `follow_up_categories` in the config.

### Combining with Other Studies

This can be paired with:
- Pre/post questionnaires
- Daily diary methods
- Longitudinal follow-ups

## Troubleshooting

**Conversation too short?**
- Check depth preference in user_info
- Verify exit_criteria in config

**Not exploring all 4 aspects?**
- Participant may not mention all naturally
- Adjust prompts to be more directive
- Increase conversation depth

**Questions too generic?**
- Add more specific examples in follow_up_categories
- Refine the approach guidelines
- Include scenario-specific probes

## Contact & Support

For questions about configuration or customization, refer to:
- `PROMPTS_GUIDE.md` - Comprehensive prompt customization guide
- `README.md` - General system documentation
