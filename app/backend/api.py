from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.core.ai_agent import create_ai_agent
from app.config.settings import Settings
from app.common.custom_exception import CustomException
from app.common.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="Multi AI Agent")


# Accept structured messages in OpenAI format
class RequestState(BaseModel):
    model_name: str
    messages: List[Dict[str, str]]   # role + content format
    allow_search: bool
    system_prompt: str


@app.post('/chat')
def chat(request: RequestState):
    logger.info(f"Request messages: {request.messages}, "
                f"Allow Search: {request.allow_search}, "
                f"System Prompt: {request.system_prompt}, "
                f"Groq API: {Settings.GROQ_API_KEY}")
    
    try:
        response = create_ai_agent(
            llm_id=request.model_name,
            messages=request.messages,   # forward structured messages
            allow_search=request.allow_search,
            system_prompt=request.system_prompt,
            groq_api_key=Settings.GROQ_API_KEY
        )

        logger.info(f"Response generated successfully from model {request.model_name}")
        return {'response': response}

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(CustomException("Failed to get AI response", error_detail=e))
        )
