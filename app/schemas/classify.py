from pydantic import BaseModel, Field


class ClassifyRequest(BaseModel):
    prompt: str = Field(..., description="Message libre saisi par l'utilisateur.")
    language: str = Field("fr", description="Langue de travail (par défaut: fr).")


class ClassifyResponse(BaseModel):
    mission: str
    confidence: float
    reasoning: str
