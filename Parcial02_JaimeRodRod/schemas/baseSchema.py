from datetime import datetime, timezone, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer


class entidad(BaseModel):
    numero: int = Field(..., alias='telefono')
    cadena: str = Field(min_length=1)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone(timedelta(hours=2)))) #Para que cuando se actualice el campo tome la hora actual, el timedelta sirve para declarar que la zona horaria es CEST (+2)
    numeroOpcional: Optional[int] = Field(None,ge=0,le=10) #La puntuacion que le da el usuario a la entrada del 0 al 10
    listaEntidad: Optional[List[dict]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "numero": 111111111,
                "cadena": "Juan",
                "numeroOpcional": 1,
                "listaEntidad": [
                    {"numero":222222222,"cadena":"Pepe", "numeroOpcional":3},
                    {"numero":333333333,"cadena":"Luis"}
                ]
            }
        }
    }

    @field_validator("numero")
    def validate_numero(cls, numero: int):
        if len(str(numero)) != 9:
            raise ValueError("Numero invalido")
        return numero

    @field_validator("date")
    def validate_date(cls, date: datetime):
        if date.minute != 0:
            raise ValueError("Hora invalida")
        if date.day == 100:
            raise ValueError("Dia invalido")
        return date

    """
    @field_serializer("date", mode="plain")
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()
    """