from http.client import HTTPException

from fastapi import APIRouter, Body
from pymongo.errors import DuplicateKeyError

import item_logic.colaborador_itemLogic as colaborador_itemLogic
from schemas.colaborador import colaborador

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC -> colaborador_itemLogic
    - SCHEMA -> colaborador
    - IDENTIFICADOR -> email
    - idENTIDAD -> habilidad
    - ENTIDAD -> habilidad
"""

@router.post("/")
async def add_colaborador(colaborador: colaborador = Body(...)):
    try:
        exists = await colaborador_itemLogic.get_colaborador_email(colaborador.email)
        if not exists:
            result = await colaborador_itemLogic.add_colaborador(colaborador)
            return result
        else:
            raise HTTPException(status_code=500,detail="Usuario ya existente")

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_colaborador(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
):
    filter = {}
    """
    if filter_str:
        filter["str"] = filter_str
    """


    items = await colaborador_itemLogic.get_colaborador(filter)

    """
    if sort_by_newest:
        items.sort(key=colaborador_itemLogic.extract_date, reverse=True)
    """

    return items

@router.get("/{email}")
async def get_colaborador_email(email: str):
    result = await colaborador_itemLogic.get_colaborador_email(email)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Usuario no encontrado")

@router.delete("/{email}")
async def delete_colaborador(email: str):
    result = await colaborador_itemLogic.delete_colaborador(email)
    return result

@router.post("/{email}/habilidades/")
async def add_habilidad_colaborador(email: str, habilidad: str):
    result = await colaborador_itemLogic.add_habilidad_colaborador(email,habilidad)
    return bool(result)

@router.get("/{email}/habilidades/")
async def get_habilidad_colaborador(email: str):
    result = await colaborador_itemLogic.get_habilidad_colaborador(email)
    return result

@router.delete("/{email}/habilidades/")
async def delete_habilidad_colaborador(email: str, habilidad: str):
    result = await colaborador_itemLogic.delete_habilidad_colaborador(email,habilidad)
    return result

@router.get("/{email}/colaboradores/")
async def get_colaboradores(email: str):
    result = await colaborador_itemLogic.get_colaboradores(email)
    return result