from datetime import datetime
from typing import Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field, field_validator
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(str):
    """Custom ObjectId type for Pydantic v2"""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ],
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x)
        ))
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class FormSubmission(BaseModel):
    """Model for form submissions stored in MongoDB"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    mission: str = Field(..., description="Mission type (contact, donation, volunteer, information)")
    values: Dict[str, Any] = Field(..., description="Form field values submitted by user")
    username: Optional[str] = Field(None, description="Username if provided")
    language: str = Field(default="fr", description="Language of submission")
    confirmation_message: str = Field(..., description="Generated confirmation message")
    submitted_at: datetime = Field(default_factory=datetime.utcnow, description="Submission timestamp")
    ip_address: Optional[str] = Field(None, description="User IP address for tracking")
    user_agent: Optional[str] = Field(None, description="User agent string")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "mission": "contact",
                "values": {
                    "nom": "Jean Dupont",
                    "email": "jean@example.com",
                    "message": "Bonjour, j'aimerais plus d'informations"
                },
                "username": "Jean Dupont",
                "language": "fr",
                "confirmation_message": "Merci Jean ! Votre message a bien été reçu.",
                "submitted_at": "2025-12-04T22:00:00Z"
            }
        }
    }

