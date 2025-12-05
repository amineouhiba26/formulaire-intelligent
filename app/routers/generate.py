from fastapi import APIRouter, HTTPException, Request

from app.constants.missions import MissionEnum, MISSIONS
from app.constants.base_fields import BASE_FIELDS_BY_MISSION
from app.schemas.generate import GenerateFieldsRequest, GenerateFieldsResponse, FormField
from app.services.ai_logic import generate_additional_fields
from app.middleware.rate_limit import limiter

router = APIRouter(tags=["ai - fields"])


@router.post("/generate-fields", response_model=GenerateFieldsResponse)
@limiter.limit("20/minute")  # 20 requests per minute per IP
def generate_fields(request: Request, payload: GenerateFieldsRequest):
    # Validation mission
    try:
        mission_enum = MissionEnum(payload.mission)
    except ValueError:
        raise HTTPException(status_code=400, detail="Mission inconnue.")

    base_fields_raw = BASE_FIELDS_BY_MISSION.get(mission_enum, [])
    base_fields = [FormField(**f) for f in base_fields_raw]

    extra_fields_raw = generate_additional_fields(
        mission=mission_enum,
        prompt=payload.prompt,
        language=payload.language,
    )
    extra_fields = [FormField(**f) for f in extra_fields_raw]

    return GenerateFieldsResponse(
        mission=mission_enum.value,
        base_fields=base_fields,
        extra_fields=extra_fields,
    )
