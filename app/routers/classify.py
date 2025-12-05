from fastapi import APIRouter, Request

from app.schemas.classify import ClassifyRequest, ClassifyResponse
from app.services.ai_logic import classify_mission_from_prompt
from app.middleware.rate_limit import limiter

router = APIRouter(tags=["ai - classify"])


@router.post("/classify", response_model=ClassifyResponse)
@limiter.limit("5/minute")  # 30 requests per minute per IP
def classify_mission(request: Request, payload: ClassifyRequest):
    result = classify_mission_from_prompt(
        prompt=payload.prompt,
        language=payload.language,
    )
    return ClassifyResponse(**result)
