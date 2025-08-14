from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import create_ai_agent
from app.config.settings import Settings
from app.common.custom_exception import CustomException
from app.common.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="Multi AI Agent")

class RequestState(BaseModel):
    model_name: str
    messages: List[str]
    allow_search: bool
    system_prompt: str


@app.post('/chat')
def chat(request: RequestState):
    logger.info(f"Received request from model {request.model_name}")
    
    if request.model_name not in Settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model name")

    try:
        response = create_ai_agent(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Response generated successfully from model {request.model_name}")
        return {'response': response}
    
    except Exception as e:
        logger.error(f"Error generating response")
        raise HTTPException(
            status_code=500,
            detail= str(CustomException("Failed to get AI response", error_detail=e))
        )