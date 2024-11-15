from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Body, Query
from pymongo.errors import DuplicateKeyError

import item_logic.tarea_itemLogic as tarea_itemLogic
from schemas.tarea import tarea

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC -> tarea_itemLogic
    - SCHEMA -> tarea
    - IDENTIFICADOR -> id
    - idENTIDAD -> email
    - ENTIDAD -> colaborador
"""

@router.post("/")
async def add_tarea(tarea: tarea = Body(...)):
    try:
        result = await tarea_itemLogic.add_tarea(tarea)
        return result

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_tarea(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
        #habilidad: Optional[str] = Query(None)
):

    filter = {}
    """
    if filter_str:
        filter["str"] = filter_str
    """


    items = await tarea_itemLogic.get_tarea(filter)

    """
    if sort_by_newest:
        items.sort(key=tarea_itemLogic.extract_date, reverse=True)
    """

    return items

@router.get("/byID/{id}")
async def get_tarea_id(id: str):
    result = await tarea_itemLogic.get_tarea_id(id)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Usuario no encontrado")

@router.delete("/{id}")
async def delete_tarea(id: str):
    result = await tarea_itemLogic.delete_tarea(id)
    return result

@router.patch("/updateTarea/{id}")
async def update_user(id: str, req: tarea = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await tarea_itemLogic.update_tarea(id,req)
    return result

@router.get("/habilidad")
async def get_tarea_habilidad(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
        habilidad: Optional[str] = Query(None)
):
    items = await tarea_itemLogic.get_tarea_habilidad(habilidad)
    return items

@router.get("/colaboradorEmail")
async def get_tarea_colaborador_email(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
        colaboradorEmail: Optional[str] = Query(None)
):
    items = await tarea_itemLogic.get_tarea_colaborador(colaboradorEmail)
    return items

@router.patch("/addColaborador")
async def add_colaborador_tarea(id: str, email: str):
    result = await tarea_itemLogic.add_colaborador_tarea(id,email)
    return bool(result)

@router.get("/posiblesColaboradores")
async def get_posibles_colaboradores_tarea(id: str):
    result = await tarea_itemLogic.get_possible_colaborador_tarea(id)
    return result

@router.get("/completamenteAsignadas")
async def get_tareas_completamente_asignadas():
    result = await tarea_itemLogic.get_tareas_completamente_asignadas()
    return result

#LISTA CAMPO IDENTIFICADOR
"""

@router.post("/{id}/colaborador/")
async def add_colaborador_tarea(id: str, email: str):
    exists = await tarea_itemLogic.get_colaborador_tarea_email(id,email)
    if not exists:
        result = await tarea_itemLogic.add_colaborador_tarea(id,email)
        return bool(result)
    else:
        raise HTTPException(status_code=500,detail="Usuario ya existente")

@router.get("/{id}/colaborador/")
async def get_colaborador_tarea(id: str):
    result = await tarea_itemLogic.get_colaborador_tarea(id)
    return result

@router.get("/{id}/colaborador/{email}")
async def get_colaborador_tarea_email(id: str, email: str):
    result = await tarea_itemLogic.get_colaborador_tarea_email(id,email)
    return result

@router.delete("/{id}/colaborador/")
async def delete_colaborador_tarea(id: str, email: str):
    result = await tarea_itemLogic.delete_colaborador_tarea(id,email)
    return result

"""