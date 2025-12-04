from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class FormField(BaseModel):
    name: str = Field(..., description="Identifiant unique du champ (snake_case).")
    label: str = Field(..., description="Texte affiché pour l'utilisateur.")
    type: Literal["text", "email", "textarea", "number", "select", "checkbox"] = "text"
    required: bool = False
    options: Optional[List[str]] = None  # seulement pour select


class GenerateFieldsRequest(BaseModel):
    mission: str = Field(..., description="Mission fixée (contact, donation, volunteer, information).")
    prompt: str = Field(..., description="Message de l'utilisateur pour enrichir le formulaire.")
    language: str = Field("fr", description="Langue de travail (par défaut: fr).")


class GenerateFieldsResponse(BaseModel):
    mission: str
    base_fields: List[FormField]
    extra_fields: List[FormField]
