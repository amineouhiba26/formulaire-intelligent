from datetime import datetime

from fastapi import APIRouter, HTTPException, Request

from app.constants.missions import MissionEnum
from app.schemas.submit import SubmitRequest, SubmitResponse
from app.services.ai_logic import generate_confirmation_message
from app.database import get_database
from app.models import FormSubmission

router = APIRouter(tags=["ai - submit"])


@router.post("/submit", response_model=SubmitResponse)
async def submit_form(payload: SubmitRequest, request: Request):
    # Validation mission
    try:
        mission_enum = MissionEnum(payload.mission)
    except ValueError:
        raise HTTPException(status_code=400, detail="Mission inconnue.")

    year = datetime.now().year

    try:
        confirmation_message = generate_confirmation_message(
            mission=mission_enum,
            values=payload.values,
            username=payload.username,
            language=payload.language,
        )
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        # Fallback message if AI fails
        confirmation_message = f"Merci {payload.username or ''} ! Votre demande pour '{mission_enum.value}' a bien été reçue."


    # Save to MongoDB
    db = get_database()
    submission = FormSubmission(
        mission=mission_enum.value,
        values=payload.values,
        username=payload.username,
        language=payload.language,
        confirmation_message=confirmation_message,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    # Insert into database
    result = await db.submissions.insert_one(submission.dict(by_alias=True, exclude={"id"}))
    
    print(f"✅ Form submission saved to MongoDB with ID: {result.inserted_id}")

    return SubmitResponse(
        mission=mission_enum.value,
        year=year,
        confirmation_message=confirmation_message,
    )

