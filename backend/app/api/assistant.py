from fastapi import APIRouter
from app.schemas.dto import AssistantPrompt
from app.services.assistant import generate_recommendations

router = APIRouter()


@router.post('/chat')
async def chat(payload: AssistantPrompt):
    data = generate_recommendations(payload.brand_name or 'Brand')
    return {'reply': f"{payload.prompt} | Advice: {data['advice']}", 'alternatives': data['alternatives']}
