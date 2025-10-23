"""
FastAPI REST API interface for the ESM Chatbot.

This provides REST endpoints for external applications to integrate with the chatbot.

Run with: uvicorn interfaces.fastapi_app:app --reload
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from core.api import ESMBot
from config.settings import get_settings

# Initialize FastAPI app
app = FastAPI(
    title="ESM Chatbot API",
    description="REST API for Experience Sampling Method Chatbot",
    version="1.0.0"
)

# Configure CORS for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize bot
settings = get_settings()
bot = ESMBot()


# Request/Response models
class SessionStartRequest(BaseModel):
    """Request to start a new session"""
    participant_id: str
    experiment_id: str
    user_info: Optional[Dict[str, Any]] = {}


class SessionStartResponse(BaseModel):
    """Response from starting a session"""
    session_id: str
    participant_id: str
    experiment_id: str
    initial_message: str


class MessageRequest(BaseModel):
    """Request to send a message"""
    session_id: str
    message: str


class MessageResponse(BaseModel):
    """Response from sending a message"""
    response: str
    session_id: str
    exchange_count: int
    is_complete: bool
    topics_covered: List[str]


class ExperimentInfo(BaseModel):
    """Information about an experiment"""
    experiment_id: str
    name: str
    description: str
    user_info_fields: List[Dict[str, Any]]


# Endpoints
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "ESM Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/experiments", response_model=List[str])
async def list_experiments():
    """
    List all available experiments.

    Returns:
        List of experiment IDs
    """
    try:
        return bot.list_experiments()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/experiments/{experiment_id}", response_model=ExperimentInfo)
async def get_experiment(experiment_id: str):
    """
    Get details about a specific experiment.

    Args:
        experiment_id: Experiment identifier

    Returns:
        Experiment information
    """
    try:
        config = bot.question_manager.get_experiment_config(experiment_id)
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experiment '{experiment_id}' not found"
            )

        user_info_fields = bot.question_manager.get_user_info_fields(experiment_id)

        return ExperimentInfo(
            experiment_id=experiment_id,
            name=config.get("name", experiment_id),
            description=config.get("description", ""),
            user_info_fields=user_info_fields
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/sessions/start", response_model=SessionStartResponse)
async def start_session(request: SessionStartRequest):
    """
    Start a new conversation session.

    Args:
        request: Session start request with participant and experiment info

    Returns:
        Session information with initial message
    """
    try:
        # Start the session
        session = bot.start_session(
            participant_id=request.participant_id,
            experiment_id=request.experiment_id,
            user_info=request.user_info
        )

        # Get initial message
        initial_msg = bot.get_initial_message(session.session_id)

        return SessionStartResponse(
            session_id=session.session_id,
            participant_id=session.participant_id,
            experiment_id=session.experiment_id,
            initial_message=initial_msg
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/messages", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    Send a message and get a response.

    Args:
        request: Message request with session ID and message content

    Returns:
        Bot response and conversation metadata
    """
    try:
        result = bot.process_message(
            session_id=request.session_id,
            message=request.message
        )

        return MessageResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/sessions/{session_id}/export")
async def export_session(session_id: str):
    """
    Export session data.

    Args:
        session_id: Session identifier

    Returns:
        Complete session data
    """
    try:
        data = bot.export_session(session_id)
        if not data or not data.get("session_data"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session '{session_id}' not found"
            )
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get session information.

    Args:
        session_id: Session identifier

    Returns:
        Session metadata
    """
    try:
        session = bot.session_manager.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session '{session_id}' not found"
            )

        return {
            "session_id": session.session_id,
            "participant_id": session.participant_id,
            "experiment_id": session.experiment_id,
            "user_info": session.user_info,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "is_active": session.is_active,
            "total_exchanges": session.total_exchanges,
            "total_messages": session.total_messages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port
    )
