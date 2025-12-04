from typing import Dict, Any, Optional

from pydantic import BaseModel, Field

from app.schemas.generate import FormField  # si besoin pour retour avancé


class SubmitRequest(BaseModel):
    mission: str = Field(..., description="Mission choisie.")
    values: Dict[str, Any] = Field(..., description="Valeurs remplies par l'utilisateur.")
    username: Optional[str] = Field(
        None, description="Nom d'utilisateur (si fourni séparément)."
    )
    language: str = Field("fr", description="Langue de réponse.")


class SubmitResponse(BaseModel):
    mission: str
    year: int
    confirmation_message: str
