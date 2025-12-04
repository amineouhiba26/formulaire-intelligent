from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.constants.missions import MissionEnum
from app.schemas.submit import SubmitRequest, SubmitResponse
from app.services.ai_logic import generate_confirmation_message

router = APIRouter(tags=["ai - submit"])


@router.post("/submit", response_model=SubmitResponse)
def submit_form(payload: SubmitRequest):
    # Validation mission
    try:
        mission_enum = MissionEnum(payload.mission)
    except ValueError:
        raise HTTPException(status_code=400, detail="Mission inconnue.")

    year = datetime.now().year

    confirmation_message = generate_confirmation_message(
        mission=mission_enum,
        values=payload.values,
        username=payload.username,
        language=payload.language,
    )

    # Ici tu pourrais aussi sauvegarder dans une DB si tu veux

    return SubmitResponse(
        mission=mission_enum.value,
        year=year,
        confirmation_message=confirmation_message,
    )
