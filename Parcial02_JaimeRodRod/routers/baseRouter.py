from http.client import HTTPException

from fastapi import APIRouter, Body
from pymongo.errors import DuplicateKeyError

#import item_logic.NOMBRE_LOGIC as NOMBRE_LOGIC
#from schemas.SCHEMA import *

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC
    - SCHEMA
    - IDENTIFICADOR
    - idENTIDAD
    - ENTIDAD
"""

@router.post("/")
async def add_SCHEMA(SCHEMA: SCHEMA = Body(...)):
    try:
        exists = await NOMBRE_LOGIC.get_SCHEMA_IDENTIFICADOR(SCHEMA.IDENTIFICADOR)
        if not exists:
            result = await NOMBRE_LOGIC.add_SCHEMA(SCHEMA)
            return result
        else:
            raise HTTPException(status_code=500,detail="Usuario ya existente")

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_SCHEMA(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
):
    filter = {}
    """
    if filter_str:
        filter["str"] = filter_str
    """


    items = await NOMBRE_LOGIC.get_SCHEMA(filter)

    """
    if sort_by_newest:
        items.sort(key=NOMBRE_LOGIC.extract_date, reverse=True)
    """

    return items

@router.get("/{IDENTIFICADOR}")
async def get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR: int):
    result = await NOMBRE_LOGIC.get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Usuario no encontrado")

@router.delete("/{IDENTIFICADOR}")
async def delete_SCHEMA(IDENTIFICADOR: int):
    result = await NOMBRE_LOGIC.delete_SCHEMA(IDENTIFICADOR)
    return result

@router.patch("/{IDENTIFICADOR}")
async def update_user(IDENTIFICADOR: int, req: SCHEMA = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await NOMBRE_LOGIC.update_SCHEMA(IDENTIFICADOR,req)
    return result

#SUBIDENTIDADES EN LA ENTIDAD CON MULTIPLES CAMPOS
"""

@router.post("/{IDENTIFICADOR}/ENTIDAD/")
async def add_ENTIDAD_SCHEMA(IDENTIFICADOR: int, ENTIDAD: ENTIDAD = Body(...)):
    exists = await NOMBRE_LOGIC.get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR,ENTIDAD.idENTIDAD)
    if not exists:
        item_data = ENTIDAD.model_dump()
        result = await NOMBRE_LOGIC.add_ENTIDAD_SCHEMA(IDENTIFICADOR,item_data)
        return result
    else:
        raise HTTPException(status_code=500,detail="Usuario ya existente")

@router.get("/{IDENTIFICADOR}/ENTIDAD/")
async def get_ENTIDAD_SCHEMA(IDENTIFICADOR: int):
    result = await NOMBRE_LOGIC.get_ENTIDAD_SCHEMA(IDENTIFICADOR)
    return result

@router.get("/{IDENTIFCADOR}/ENTIDAD/{idENTIDAD}")
async def get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR: int, idENTIDAD: int):
    result = await NOMBRE_LOGIC.get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR,idENTIDAD)
    return result

@router.delete("/{IDENTIFICADOR}/ENTIDAD/")
async def delete_ENTIDAD_SCHEMA(IDENTIFICADOR: int, idENTIDAD: int):
    result = await NOMBRE_LOGIC.delete_ENTIDAD_SCHEMA(IDENTIFICADOR,idENTIDAD)
    return result

@router.patch("/{IDENTIFICADOR}/ENTIDAD/")
async def update_ENTIDAD_SCHEMA(IDENTIFICADOR: int, req: ENTIDAD = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await NOMBRE_LOGIC.update_ENTIDAD_SCHEMA(IDENTIFICADOR, req)
    return result

"""

#LISTA CAMPO IDENTIFICADOR
"""

@router.post("/{IDENTIFICADOR}/ENTIDAD/")
async def add_ENTIDAD_SCHEMA(IDENTIFICADOR: int, idENTIDAD: int):
    exists = await NOMBRE_LOGIC.get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR,idENTIDAD)
    if not exists:
        result = await NOMBRE_LOGIC.add_ENTIDAD_SCHEMA(IDENTIFICADOR,idENTIDAD)
        return bool(result)
    else:
        raise HTTPException(status_code=500,detail="Usuario ya existente")

@router.get("/{IDENTIFICADOR}/ENTIDAD/")
async def get_ENTIDAD_SCHEMA(IDENTIFICADOR: int):
    result = await NOMBRE_LOGIC.get_ENTIDAD_SCHEMA(IDENTIFICADOR)
    return result

@router.get("/{IDENTIFICADOR}/ENTIDAD/{idENTIDAD}")
async def get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR: int, idENTIDAD: int):
    result = await NOMBRE_LOGIC.get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR,idENTIDAD)
    return result

@router.delete("/{IDENTIFICADOR}/ENTIDAD/")
async def delete_ENTIDAD_SCHEMA(IDENTIFICADOR: int, idENTIDAD: int):
    result = await NOMBRE_LOGIC.delete_ENTIDAD_SCHEMA(IDENTIFICADOR,idENTIDAD)
    return result

"""