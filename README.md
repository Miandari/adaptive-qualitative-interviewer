# ESM Chatbot - Experience Sampling Method Conversational System

A flexible, integration-ready chatbot for conducting Experience Sampling Method (ESM) research studies. Built with LangGraph for intelligent conversation flow and designed for easy deployment and integration into existing applications.

## Features

- **Dynamic Conversational Flow**: Uses LangGraph to create adaptive conversations that intelligently follow up based on participant responses
- **Flexible Integration**: Multiple deployment options including standalone UI, REST API, and Python library
- **ESM-Optimized**: Purpose-built for experience sampling research with configurable experiments
- **Session Management**: Robust user session tracking with participant information
- **Data Export**: Easy export to JSON and CSV formats for analysis
- **Modular Architecture**: Core logic can be imported and integrated into existing applications

## Project Structure

```
esm_chatbot/
├── core/                   # Core conversation logic (importable library)
│   ├── graph/             # LangGraph flow components
│   │   ├── state.py       # State management
│   │   ├── nodes.py       # Conversation nodes
│   │   └── edges.py       # Flow control logic
│   ├── esm/               # ESM-specific components
│   │   ├── session.py     # Session management
│   │   ├── prompts.py     # Prompt building
│   │   └── questions.py   # Question management
│   └── api.py             # Main ESMBot API
├── interfaces/            # Different UI/API options
│   ├── streamlit_app.py   # Streamlit web interface (primary)
│   └── fastapi_app.py     # REST API
├── config/
│   ├── settings.py        # Application settings
│   └── experiments.yaml   # Experiment definitions
├── storage/
│   └── memory.py          # In-memory storage (replaceable)
└── examples/              # Usage examples
    ├── standalone.py      # Python library usage
    ├── api_client.py      # REST API client
    └── export_data.py     # Data export utility
```

## Quick Start

### 1. Installation

```bash
# Clone or navigate to the project
cd esm_chatbot

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your LLM API keys
```

### 2. Configure Your API Keys

Edit `.env` file:

```bash
# Choose your provider
OPENAI_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here

LLM_PROVIDER=openai  # or anthropic
LLM_MODEL=gpt-4o     # or claude-3-5-sonnet-20241022
```

### 3. Run the Chatbot

**Option A: Streamlit Web Interface (Recommended for getting started)**

```bash
streamlit run interfaces/streamlit_app.py
```

Then open http://localhost:8501 in your browser.

**Option B: REST API Server**

```bash
uvicorn interfaces.fastapi_app:app --reload
```

API docs available at http://localhost:8000/docs

**Option C: Python Library**

```python
from core.api import ESMBot

bot = ESMBot()
session = bot.start_session(
    participant_id="user_001",
    experiment_id="empathy_study",
    user_info={"participant_id": "user_001"}
)
```

## Configuration

### Defining Experiments

Edit `config/experiments.yaml` to define your ESM studies:

```yaml
experiments:
  your_study_name:
    name: "Your Study Title"
    description: "Study description"

    # Participant info to collect
    user_info_fields:
      - name: "participant_id"
        type: "text"
        required: true
        prompt: "Enter your Participant ID"

    # Initial question
    initial_question:
      text: "Your opening question here"
      context: "Context/instructions for participants"

    # Research goals (guides conversation)
    goals:
      - "Goal 1"
      - "Goal 2"

    # Follow-up categories
    follow_up_categories:
      category_name:
        description: "What this explores"
        example_questions:
          - "Example question 1"
          - "Example question 2"

    # Conversation guidelines
    conversation_guidelines:
      tone: "warm and curious"
      style: "conversational"
      approach: |
        Instructions for how the chatbot should conduct the conversation...

      exit_criteria:
        - "When to end the conversation"
```

## Usage Examples

### 1. As a Python Library

```python
from core.api import ESMBot

# Initialize
bot = ESMBot()

# Start session
session = bot.start_session(
    participant_id="p001",
    experiment_id="empathy_study",
    user_info={"participant_id": "p001", "age": 25}
)

# Get initial message
initial = bot.get_initial_message(session.session_id)
print(f"Bot: {initial}")

# Process messages
result = bot.process_message(
    session_id=session.session_id,
    message="I talked with my friend today..."
)
print(f"Bot: {result['response']}")

# Export data
data = bot.export_session(session.session_id)
```

See `examples/standalone.py` for a complete example.

### 2. Via REST API

```python
import requests

# Start session
response = requests.post(
    "http://localhost:8000/sessions/start",
    json={
        "participant_id": "p001",
        "experiment_id": "empathy_study",
        "user_info": {"participant_id": "p001"}
    }
)
session_data = response.json()

# Send message
response = requests.post(
    "http://localhost:8000/messages",
    json={
        "session_id": session_data["session_id"],
        "message": "Your message here"
    }
)
result = response.json()
```

See `examples/api_client.py` for a complete client implementation.

### 3. Embedding in Your Application

The core ESMBot can be integrated into existing applications:

```python
# In your application
from core.api import ESMBot

class YourApp:
    def __init__(self):
        self.esm_bot = ESMBot(
            experiment_config_path="path/to/your/config.yaml"
        )

    def handle_esm_session(self, user_id):
        session = self.esm_bot.start_session(
            participant_id=user_id,
            experiment_id="your_experiment",
            user_info=self.get_user_info(user_id)
        )
        return session
```

## API Endpoints

When running the FastAPI server:

- `GET /experiments` - List available experiments
- `GET /experiments/{id}` - Get experiment details
- `POST /sessions/start` - Start a new session
- `POST /messages` - Send a message
- `GET /sessions/{id}` - Get session info
- `GET /sessions/{id}/export` - Export session data

Full API documentation at `http://localhost:8000/docs`

## Data Export

### Export from Streamlit UI

Use the export functionality in the Streamlit interface.

### Export via API

```python
data = bot.export_session(session_id)

# Save to JSON
import json
with open('session.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Export to CSV

```bash
python examples/export_data.py --format csv --output results.csv --data-file session.json
```

## Customization

### Using Different LLM Providers

The system supports OpenAI and Anthropic models:

```python
# OpenAI
bot = ESMBot(llm_provider="openai", llm_model="gpt-4o")

# Anthropic
bot = ESMBot(llm_provider="anthropic", llm_model="claude-3-5-sonnet-20241022")
```

### Custom Storage Backend

Replace the in-memory storage with your own:

```python
from storage.memory import InMemoryStorage

class DatabaseStorage(InMemoryStorage):
    def store_message(self, session_id, role, content, metadata):
        # Your database logic here
        pass
```

### Modifying Conversation Flow

Edit `core/graph/nodes.py` to customize conversation logic:

- Modify question generation
- Add new conversation stages
- Implement custom follow-up logic

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# For Streamlit
CMD ["streamlit", "run", "interfaces/streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

# OR for API
# CMD ["uvicorn", "interfaces.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Streamlit Community Cloud (Recommended)

**Free, easy deployment directly from GitHub:**

1. **Prepare your repository** (already done!):
   - Dependencies pinned in `requirements.txt`
   - Configuration in `.streamlit/config.toml`
   - Secrets template in `.streamlit/secrets.toml.example`

2. **Deploy to Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `adaptive-qualitative-interviewer`
   - Main file path: `interfaces/streamlit_app.py`
   - Click "Deploy"

3. **Add your secrets** in the Streamlit Cloud dashboard:
   - Go to app settings → Secrets
   - Add your API keys:
     ```toml
     OPENAI_API_KEY = "sk-your-key-here"
     LLM_PROVIDER = "openai"
     LLM_MODEL = "gpt-4o"
     ```
   - Or for Anthropic:
     ```toml
     ANTHROPIC_API_KEY = "sk-ant-your-key-here"
     LLM_PROVIDER = "anthropic"
     LLM_MODEL = "claude-3-5-sonnet-20241022"
     ```

4. **Your app will be live at:**
   ```
   https://your-app-name.streamlit.app
   ```

**Auto-deployment:** Push to GitHub → App automatically updates!

### Other Cloud Options

- **Railway**: https://railway.app (free tier available)
- **Render**: https://render.com (free tier available)
- **Heroku**: Traditional deployment (~$7/month)
- **University/Institution Server**: Use Docker deployment (see above)

## Research Considerations

### Data Privacy

- Configure session storage appropriately for your IRB requirements
- Implement authentication if needed
- Consider HIPAA/GDPR compliance for your use case

### Study Design

- Test conversation flows before deployment
- Validate question sequences
- Monitor conversation quality
- Export and analyze pilot data

### Integration Options

1. **Standalone Web App**: Use Streamlit interface directly
2. **Embedded Widget**: Integrate via iframe or JavaScript SDK
3. **Backend Integration**: Use as Python library in your app
4. **Microservice**: Deploy API separately and integrate via HTTP

## Troubleshooting

### LLM API Issues

```python
# Check your API key
import os
print(os.getenv('OPENAI_API_KEY'))

# Test connection
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("test")
```

### Module Import Errors

Ensure you're running from the project root:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python examples/standalone.py
```

## Development

### Running Tests

```bash
# Add tests as needed
pytest tests/
```

### Adding New Features

1. Core logic goes in `core/`
2. UI/API changes in `interfaces/`
3. Configuration in `config/`
4. Update examples and README

## Future Enhancements

- [ ] Database persistence (PostgreSQL, MongoDB)
- [ ] Multi-language support
- [ ] Audio/video integration
- [ ] Real-time analytics dashboard
- [ ] Embeddable JavaScript widget
- [ ] Mobile app interface

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Citation

If you use this in your research, please cite:

```
[Add citation information]
```

## Support

For issues and questions:
- Open an issue on GitHub
- Contact: [your contact info]

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit](https://streamlit.io)
- [FastAPI](https://fastapi.tiangolo.com/)
