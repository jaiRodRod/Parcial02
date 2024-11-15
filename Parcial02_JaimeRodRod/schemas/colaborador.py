from datetime import datetime, timezone, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer


class colaborador(BaseModel):
    email: str = Field(...)
    nombre: str = Field(min_length=1)
    habilidades: Optional[List[str]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "juan@uma.es",
                "nombre": "Juan",
                "habilidades": [
                    "sociable",
                    "creativo"
                ]
            }
        }
    }

    @field_validator("email")
    def validate_email(cls, email: str):
        if not "@" in email:
            raise ValueError("Email invalido")
        return email