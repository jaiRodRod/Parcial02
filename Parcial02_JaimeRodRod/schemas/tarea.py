from datetime import datetime, timezone, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer


class tarea(BaseModel):
    responsable: str = Field(...)
    descripcion: str = Field(max_length=50)
    habilidades: Optional[List[str]] = []
    segmentos: int = Field(...)
    colaboradores: Optional[List[str]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "responsable": "juan@uma.es",
                "descripcion": "Una tarea enfocada al examen",
                "habilidades": [
                    "valor",
                    "conocimiento web"
                ],
                "segmentos": 10,
                "colaboradores": [
                    "juan@uma.es",
                    "pepe@uma.es"
                ]
            }
        }
    }

    @field_validator("responsable")
    def validate_email(cls, email: str):
        if not "@" in email:
            raise ValueError("Email invalido")
        return email