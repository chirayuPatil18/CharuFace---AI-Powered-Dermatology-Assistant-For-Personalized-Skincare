from fastapi import APIRouter
from pydantic import BaseModel
from chatbot.chat_pipeline import chat_with_ai

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    email: str


@router.post("/chat")
def chat(req: ChatRequest):
    reply = chat_with_ai(req.message, req.email)
    return {"reply": reply}