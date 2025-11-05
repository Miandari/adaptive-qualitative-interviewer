# AI Experimenter - Development Guide

## Project Overview

**Current State:** AI Experimenter is an Experience Sampling Method (ESM) research chatbot built with LangChain/LangGraph. It conducts qualitative research interviews through conversational AI, currently supporting studies on empathy and decision-making.

**Vision:** Transform into a multi-user research framework where researchers can:
- Create and load their own experiments without modifying core code
- Customize conversation flows, data collection, and evaluation criteria
- Share experiments with other researchers
- Run isolated experiments with private prompts

## Architecture Foundation

**Core Technologies:**
- LangChain/LangGraph for conversation orchestration
- OpenAI/Anthropic LLM providers
- Multiple UI options (Streamlit primary, FastAPI for REST API)
- YAML-based experiment configuration
- Python 3.x with virtual environment (venv)

**Development Environment:**
- Uses virtual environment located in `venv/`
- Activate with: `source venv/bin/activate`
- Always use `venv/bin/python` or activate venv before running Python commands
- Dependencies managed via `requirements.txt`

**Current Structure:**
```
core/                  # Core conversation engine
├── api.py            # Main ESMBot API
├── esm/              # Experiment management
│   ├── prompts.py    # Prompt builders
│   ├── questions.py  # Config management
│   └── session.py    # Session tracking
└── graph/            # LangGraph conversation flow
    ├── state.py      # State schema
    ├── nodes.py      # Conversation nodes
    └── edges.py      # Flow control

config/               # Configuration
└── experiments.yaml  # Experiment definitions

interfaces/           # Multiple UIs
├── streamlit_app.py  # Primary web interface
└── fastapi_app.py    # REST API
```

## Development Roadmap

### Phase 1: Prepare for Public Repository (Current)

**Goal:** Make repository public while keeping proprietary prompts private

**Tasks:**
- [x] Verify .env security (confirmed safe - never committed)
- [ ] Create experiment separation structure
- [ ] Move experiments to separate files
- [ ] Update experiment loading system
- [ ] Create public example experiments
- [ ] Update .gitignore for private experiments
- [ ] Write documentation for creating experiments

**Key Changes:**
- Restructure `config/experiments.yaml` → `experiments/` directory
- Support loading experiments from multiple sources
- Keep private experiments in gitignored directories

### Phase 2: Experiment Packaging System (Next 1-2 months)

**Goal:** Enable researchers to create, share, and load their own experiments

**Tasks:**
- [ ] Design experiment package format
- [ ] Create `ExperimentLoader` abstraction
  - File loader (local YAML files)
  - URL loader (remote experiments)
  - Environment variable loader (for secrets)
- [ ] Implement experiment discovery mechanism
- [ ] Add experiment validation (JSON schema)
- [ ] Create experiment export/import utilities
- [ ] Build experiment templates
- [ ] Write comprehensive experiment creation guide

**Key Features:**
- Load experiments from: files, URLs, environment variables
- Validate experiment structure before loading
- Support experiment versioning and metadata
- Enable easy sharing of experiment definitions

### Phase 3: Plugin Architecture (3-6 months)

**Goal:** Allow customization beyond YAML configuration

**Current Limitations:**
- Fixed 3-stage conversation flow (initial → exploration → closing)
- Hard-coded exit logic (exchange counting)
- No custom conversation nodes or branching
- Fixed state schema (can't add custom fields)
- Limited data collection points

**Tasks:**
- [ ] Create `Experiment` class with proper abstraction
- [ ] Implement dynamic graph builder
  - Define conversation flow in config
  - Support custom stages and branching
  - Enable conditional logic
- [ ] Design plugin interface (`ExperimentPlugin` ABC)
- [ ] Implement plugin discovery and loading
- [ ] Create extensible state schema
- [ ] Add custom node/edge support
- [ ] Build example plugins:
  - Custom conversation nodes
  - Custom exit evaluators
  - Custom data exporters
- [ ] Write plugin development documentation

**Architectural Changes:**
- Replace hard-coded graph in `core/api.py` with dynamic builder
- Change fixed TypedDict state to extensible schema
- Add plugin system for custom behavior
- Support experiment-specific Python code

### Phase 4: Multi-User Framework (6+ months, optional)

**Goal:** Support multiple researchers with isolated experiments and data

**Tasks:**
- [ ] Add researcher/organization model
- [ ] Implement multi-tenancy and data isolation
- [ ] Add authentication/authorization layer
- [ ] Create experiment ownership system
- [ ] Build experiment marketplace/registry
- [ ] Add experiment search and discovery
- [ ] Implement experiment dependency management
- [ ] Create collaboration features

**Key Features:**
- Isolated data per researcher/organization
- Experiment sharing and permissions
- Marketplace for discovering experiments
- Version control and dependency management

## Current Capabilities & Limitations

### What Can Be Customized Now (YAML only):
- Question text and context
- Conversation tone, style, approach
- Follow-up categories and example questions
- Research goals
- User demographic fields
- Exit criteria text (documentation only)

### What Requires Code Changes:
- Conversation flow structure (3 stages are hard-coded)
- Exit logic implementation
- Topic tracking and categorization
- Data collection points
- Message metadata structure
- Storage schema
- Export formats

### Hard-Coded Assumptions:
- 3-stage linear conversation model
- Single session per participant
- Keyword-based topic detection
- Exchange-based exit criteria
- Synchronous text-only interaction

## Coding Standards

### General Principles
- **No emojis** unless explicitly necessary for the feature
- Write clear, self-documenting code
- Prefer explicit over implicit
- Keep functions focused and single-purpose
- Maintain backward compatibility when possible

### Python Style
- Follow PEP 8 conventions
- Use type hints for function signatures
- Write comprehensive docstrings for public APIs
- Use meaningful variable and function names
- Prefer composition over inheritance

### Documentation
- Update this file when making architectural decisions
- Document why, not just what
- Keep README.md user-focused
- Maintain inline comments for complex logic
- Add examples for new features

### Testing
- Write tests for new functionality
- Test edge cases and error conditions
- Maintain test coverage as features are added
- Document test requirements in experiment definitions

## Architecture Decisions

### Why LangGraph?
- Native support for stateful conversations
- Flexible node/edge model for conversation flow
- Built-in state management
- Easy to extend and customize

### Why Separate Interfaces?
- Different deployment needs (local vs cloud)
- Different user preferences (web vs API)
- Allows independent evolution of UIs
- Core logic remains interface-agnostic

### Why YAML for Experiments?
- Human-readable and editable
- Easy for non-programmers to modify
- Good for version control
- Can be validated with schemas
- Will evolve to support more formats (JSON, Python DSL)

### Design Trade-offs

**Current: Simplicity vs Flexibility**
- Chose simplicity for initial version
- Fixed 3-stage flow is easy to understand
- Trade-off: Limits experiment types
- Solution: Phase 3 will add flexibility while maintaining simple path

**YAML vs Database for Experiments**
- Chose YAML for simplicity and version control
- Trade-off: No query capabilities, limited to file size
- Solution: Phase 4 can add database support while keeping YAML option

**In-Memory vs Persistent Storage**
- Chose in-memory for simplicity and privacy
- Trade-off: Data lost on restart
- Current: Intentional for privacy in research
- Solution: Already abstracted, can swap storage backends

## Technical Notes

### Extension Points (Current)
- LLM provider (OpenAI/Anthropic, can add more)
- Storage backend (in-memory, can add database)
- UI framework (Streamlit/FastAPI, can add more)
- Prompt templates (in YAML, easily customizable)

### Integration Considerations
- **Streamlit Cloud:** Works well, use secrets for API keys and private experiments
  - **IMPORTANT:** After updating secrets, you MUST clear Streamlit's cache
  - Use the "Clear Cache & Reload" button in the sidebar, OR manually reboot the app
  - The bot is cached with `@st.cache_resource`, so it won't see new secrets until cache is cleared
  - Private experiments load from `EXPERIMENT_{ID}_YAML` environment variables
- **Local Development:** Use .env file (already gitignored)
- **Multi-User:** Will need authentication and database
- **API Access:** FastAPI interface ready for programmatic use

### Performance Notes
- Current: Synchronous, single conversation at a time
- LangGraph supports async (can be enabled later)
- In-memory storage is fast but not scalable
- Consider Redis/PostgreSQL for multi-user deployment

## Experiment Creation Guide (Quick Reference)

### Current Format (experiments.yaml)
```yaml
experiments:
  study_name:
    name: "Study Display Name"
    description: "Study description"

    user_info_fields:
      - name: "field_name"
        type: "text|number|select"
        required: true
        prompt: "Question to ask"

    initial_question:
      text: "Opening question"
      context: "Scenario or background"

    goals:
      - "Research objective 1"
      - "Research objective 2"

    follow_up_categories:
      category_name:
        description: "What this category explores"
        example_questions:
          - "Example question 1"
          - "Example question 2"

    conversation_guidelines:
      tone: "conversational and warm"
      style: "open-ended questions"
      approach: "How to conduct the interview"
      probing_approach: "When to probe deeper"
      exit_criteria: "When to end (documentation)"
```

### Future Format (Phase 2+)
Will support:
- Multiple file formats (YAML, JSON, Python DSL)
- Custom conversation stages
- Conditional branching logic
- Custom validation rules
- Plugin references

## TODO List

### Immediate (Week 1-2)
- [ ] Create `experiments/` directory structure
- [ ] Split experiments.yaml into separate files
- [ ] Create public example experiments (sanitized)
- [ ] Update QuestionManager to load from directory
- [ ] Add experiments/private/ to .gitignore
- [ ] Write experiments/README.md with creation guide
- [ ] Test loading experiments from multiple sources

### Short-term (Month 1-2)
- [ ] Design experiment package format with metadata
- [ ] Create ExperimentLoader abstraction layer
- [ ] Implement file, URL, and env var loaders
- [ ] Add JSON schema validation for experiments
- [ ] Create experiment export/import CLI tools
- [ ] Build experiment templates for common patterns
- [ ] Write comprehensive documentation
- [ ] Add experiment versioning support

### Medium-term (Month 3-6)
- [ ] Design and implement Experiment class
- [ ] Build dynamic graph builder from config
- [ ] Create plugin interface specification
- [ ] Implement plugin discovery system
- [ ] Add support for custom conversation stages
- [ ] Create extensible state schema
- [ ] Build example plugins (nodes, evaluators, exporters)
- [ ] Write plugin development guide
- [ ] Add experiment testing framework

### Long-term (Month 6+)
- [ ] Design multi-tenancy architecture
- [ ] Add authentication/authorization
- [ ] Implement experiment ownership model
- [ ] Build experiment marketplace/registry
- [ ] Add experiment search and discovery
- [ ] Create collaboration features
- [ ] Implement experiment dependency management
- [ ] Add advanced features (branching, scheduling, multi-modal)

## Common Issues and Troubleshooting

### Streamlit Cloud: Experiments Not Loading from Secrets

**Problem:** Added experiment to secrets but it's not showing up in the app.

**Solution:**
1. Verify secret variable name is exactly: `EXPERIMENT_{ID}_YAML` (uppercase with underscores)
2. Check YAML formatting - use triple quotes `'''` correctly
3. **Clear Streamlit cache** - this is the most common issue!
   - Click "Clear Cache & Reload" button in sidebar
   - OR reboot app from "Manage app"
4. Check logs in "Manage app" for error messages

**Why this happens:** The bot is cached with `@st.cache_resource`. When secrets are added/updated, the cached bot doesn't see the new environment variables until cache is cleared.

### Streamlit Cloud: AttributeError 'NoneType' object has no attribute 'get'

**Problem:** App crashes after filling out participant info form.

**Cause:** Experiment config couldn't be found (usually due to cache issue).

**Solution:**
1. Clear cache using the sidebar button
2. Check that experiment actually loaded (see "Debug Info" in sidebar)
3. If only showing 1 experiment when you expect 2, see "Experiments Not Loading" above

### Local Development: Experiments Not Loading

**Problem:** Running locally and experiments not found.

**Solution:**
1. Check that `experiments/` directory exists with `examples/` and/or `private/` subdirectories
2. Verify YAML files are in correct locations
3. Check for YAML syntax errors (indentation, etc.)
4. Run `venv/bin/python test_experiment_loading.py` to diagnose

### YAML Parsing Errors

**Common Issues:**
- Indentation must use spaces (2 spaces per level), not tabs
- Multi-line strings require `|` or `>` operators
- Lists start with `- ` (dash + space)
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
```

## Questions to Revisit

1. **Should we support experiment inheritance/composition?**
   - Would allow DRY principle for similar experiments
   - Consider for Phase 2 or 3

2. **What database for multi-user deployment?**
   - PostgreSQL for structured data?
   - MongoDB for flexible schemas?
   - Hybrid approach?

3. **How to handle experiment versioning conflicts?**
   - Semantic versioning for experiments?
   - Backward compatibility guarantees?

4. **Should plugins be sandboxed?**
   - Security vs flexibility trade-off
   - Consider for Phase 3

5. **What license for public release?**
   - MIT for maximum adoption?
   - Apache 2.0 for patent protection?
   - Consider before Phase 1 completion

## Notes for Future Development

### When Adding Features
1. Check if it can be done in config first (YAML)
2. If not, consider if it should be a plugin
3. Only add to core if truly universal
4. Maintain backward compatibility
5. Update this file with decision rationale

### Before Major Refactoring
1. Review current usage patterns
2. Plan migration path for existing experiments
3. Consider creating compatibility layer
4. Document breaking changes clearly
5. Provide migration tools/scripts

### When Reviewing PRs
1. Check against coding standards
2. Ensure documentation is updated
3. Verify backward compatibility
4. Look for extension points
5. Consider impact on roadmap phases

---

**Last Updated:** 2025-11-04
**Current Phase:** Phase 1 - Preparing for Public Repository
**Next Milestone:** Experiment separation and multi-source loading
