import os
from typing import List

import motor
from bson import ObjectId
from motor import motor_asyncio
from dotenv import load_dotenv

from item_logic.colaborador_itemLogic import get_colaborador, get_colaborador_email
from schemas.tarea import tarea

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION -> tareas
    - SCHEMA -> tarea
    - IDENTIFICADOR -> id
    - idENTIDAD -> email
    - LISTA_ENTIDAD -> colaboradores
    - ENTIDAD -> colaborador
    - CAMPO_ACTUALIZAR //
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
tareas_collection = database["tareas"]

async def add_tarea(tarea):
    tarea_data = tarea.model_dump()
    item = await tareas_collection.insert_one(tarea_data)
    return True

async def update_tarea(id: str, tarea):
    if not tarea:
        return False
    item = await tareas_collection.find_one({"_id": ObjectId(id)})
    if item:
        updatedItem = await tareas_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": tarea}
        )
        return bool(updatedItem)
    else:
        return False

async def delete_tarea(id: str):
    deleted = False
    item = await tareas_collection.find_one({"_id": ObjectId(id)})
    if item:
        await tareas_collection.delete_one({"_id": ObjectId(id)})
        deleted = True
    return deleted


async def get_tarea(filter):
    results = []
    if len(filter) > 0:
        cursor = tareas_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in tareas_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_tarea_id(id: str) -> dict:
    item = await tareas_collection.find_one({"_id": ObjectId(id)})
    if item:
        item["_id"] = str(item["_id"])
        return item

async def get_tarea_habilidad(habilidad: str):
    results = []
    tareas = await get_tarea({})
    for tarea in tareas:
        if habilidad in tarea["habilidades"]:
            results.append(tarea)
    return results

async def get_tarea_colaborador(colaboradorEmail: str):
    results = []
    tareas = await get_tarea({})
    for tarea in tareas:
        if colaboradorEmail in tarea["colaboradores"]:
            results.append(tarea)
    return results

def match_habilidades_tarea_colaborador(habilidades_tarea:List[str], habilidades_colaborador:List[str]):
    result = False
    for habilidad in habilidades_tarea:
        if habilidad in habilidades_colaborador:
            result = True
    return result

async def add_colaborador_tarea(id: str,email: str):
    result = False
    tarea = await tareas_collection.find_one({'_id': ObjectId(id)})
    colaborador = await get_colaborador_email(email)
    if tarea and colaborador and match_habilidades_tarea_colaborador(tarea["habilidades"], colaborador["habilidades"]):
        tarea["colaboradores"].append(email)
        result = await tareas_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": tarea},
        )
    return result

async def get_possible_colaborador_tarea(id: str):
    result = []
    tarea = await tareas_collection.find_one({'_id': ObjectId(id)})
    colaboradores = await get_colaborador({})
    if tarea:
        for colaborador in colaboradores:
            if match_habilidades_tarea_colaborador(tarea["habilidades"], colaborador["habilidades"]):
                result.append(colaborador)
    return result

async def get_tareas_completamente_asignadas():
    result = []
    tareas = await get_tarea({})
    for tarea in tareas:
        if tarea["segmentos"] <= len(tarea["colaboradores"]):
            result.append(tarea)
    return result