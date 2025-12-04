from fastapi import APIRouter

from app.schemas.classify import ClassifyRequest, ClassifyResponse
from app.services.ai_logic import classify_mission_from_prompt

router = APIRouter(tags=["ai - classify"])


@router.post("/classify", response_model=ClassifyResponse)
def classify_mission(payload: ClassifyRequest):
    result = classify_mission_from_prompt(
        prompt=payload.prompt,
        language=payload.language,
    )
    return ClassifyResponse(**result)
