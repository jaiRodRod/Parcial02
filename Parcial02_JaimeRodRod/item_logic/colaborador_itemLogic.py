import os
import motor
from motor import motor_asyncio
from dotenv import load_dotenv
from schemas.colaborador import colaborador
#from item_logic.tarea_itemLogic import get_tarea

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION -> colaboradores
    - SCHEMA -> colaborador
    - IDENTIFICADOR -> email
    - idENTIDAD -> 
    - LISTA_ENTIDAD -> habilidades
    - ENTIDAD -> habilidad
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
colaboradores_collection = database["colaboradores"]
tareas_collection = database["tareas"]

colaboradores_collection.create_index("email", unique=True)

async def add_colaborador(colaborador):
    colaborador_data = colaborador.model_dump()
    item = await colaboradores_collection.insert_one(colaborador_data)
    return True

async def delete_colaborador(email: str):
    deleted = False
    item = await colaboradores_collection.find_one({"email": email})
    if item:
        await colaboradores_collection.delete_one({"email": email})
        deleted = True
    return deleted


async def get_colaborador(filter):
    results = []
    if len(filter) > 0:
        cursor = colaboradores_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in colaboradores_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_colaborador_email(email: str) -> dict:
    item = await colaboradores_collection.find_one({"email": email})
    if item:
        item["_id"] = str(item["_id"])
        return item

async def update_colaborador(email: str, colaborador):
    if not colaborador:
        return False
    item = await colaboradores_collection.find_one({"email": email})
    if item:
        updatedItem = await colaboradores_collection.update_one(
            {"email": email}, {"$set": colaborador}
        )
        return bool(updatedItem)
    else:
        return False

async def add_habilidad_colaborador(email: str,habilidad: str):
    result = False
    existe_colaborador = await colaboradores_collection.find_one({'email': email})
    if existe_colaborador:
        result = await colaboradores_collection.update_one(
            {"email": email},
            {"$push": {"habilidades": habilidad}},
        )
    return result

async def get_habilidad_colaborador(email: str):
    colaborador = await get_colaborador_email(email)
    habilidades = []
    habilidades = colaborador["habilidades"]
    return habilidades

async def delete_habilidad_colaborador(email: str, habilidad: str):
    colaborador = await colaboradores_collection.find_one({"email": email})
    for habilidadColab in colaborador["habilidades"]:
        if habilidadColab == habilidad:
            colaborador["habilidades"].remove(habilidad)
            await update_colaborador(email, colaborador)
            return True
    return False

async def get_colaboradores(email: str):
    filter =  {"responsable": email}
    tareas = []
    if len(filter) > 0:
        cursor = tareas_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            tareas.append(document)
    result = []
    for tarea in tareas:
        for colaborador in tarea["colaboradores"]:
            if colaborador not in result:
                result.append(colaborador)
    return result