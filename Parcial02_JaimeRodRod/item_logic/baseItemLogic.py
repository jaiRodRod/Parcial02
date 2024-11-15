import os
import motor
from motor import motor_asyncio
from dotenv import load_dotenv
#from schemas.SCHEMA import *

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION
    - SCHEMA
    - IDENTIFICADOR
    - idENTIDAD
    - LISTA_ENTIDAD
    - ENTIDAD
    - CAMPO_ACTUALIZAR
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
NOMBRE_COLLECTION_collection = database["NOMBRE_COLLECTION"]

#NOMBRE_COLLECTION_collection.create_index("IDENTIFICADOR", unique=True)

async def add_SCHEMA(SCHEMA):
    SCHEMA_data = SCHEMA.model_dump()
    item = await NOMBRE_COLLECTION_collection.insert_one(SCHEMA_data)
    return True

async def update_SCHEMA(IDENTIFICADOR: int, SCHEMA):
    if not SCHEMA:
        return False
    item = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    if item:
        updatedItem = await NOMBRE_COLLECTION_collection.update_one(
            {"IDENTIFICADOR": IDENTIFICADOR}, {"$set": SCHEMA}
        )
        return bool(updatedItem)
    else:
        return False

async def delete_SCHEMA(IDENTIFICADOR: int):
    deleted = False
    item = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    if item:
        await NOMBRE_COLLECTION_collection.delete_one({"IDENTIFICADOR": IDENTIFICADOR})
        deleted = True
    return deleted


async def get_SCHEMA(filter):
    results = []
    if len(filter) > 0:
        cursor = NOMBRE_COLLECTION_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in NOMBRE_COLLECTION_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR: int) -> dict:
    item = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    if item:
        item["_id"] = str(item["_id"])
        return item

def extract_date(commentary):
    try:
        fullDate = str(commentary['date'])
        dateSplitBase = fullDate.split(' ')
        yearMonthDay = dateSplitBase[0].split('-')
        dateSplitRest = dateSplitBase[1].split('.')
        hourMinuteSecond = dateSplitRest[0].split(':')

        # Crear el valor único cronológicamente ordenado
        unique_value = (
            f"{int(yearMonthDay[0]):04}"  # Año (4 dígitos)
            f"{int(yearMonthDay[1]):02}"  # Mes (2 dígitos)
            f"{int(yearMonthDay[2]):02}"  # Día (2 dígitos)
            f"{int(hourMinuteSecond[0]):02}"  # Hora (2 dígitos)
            f"{int(hourMinuteSecond[1]):02}"  # Minuto (2 dígitos)
            f"{int(hourMinuteSecond[2]):02}"  # Segundo (2 dígitos)
        )

        return int(unique_value)  # Convertir a entero para mantener orden cronológico
    except KeyError:
        return 0

#SUBIDENTIDAD MULTIPLES CAMPOS
"""
Usar cuando hay una subentidad con multiples campos (crear una clase en el schema)


  ! Si es una subidentidad del mismo formato que SCHEMA ->
        - Revisar cuando se hace ENTIDAD[idENTIDAD]
        

async def add_ENTIDAD_SCHEMA(IDENTIFICADOR: int,ENTIDAD: dict):
    result = False
    existe_SCHEMA = await NOMBRE_COLLECTION_collection.find_one({'IDENTIFICADOR': IDENTIFICADOR})
    existe_ENTIDAD = await NOMBRE_COLLECTION_collection.find_one({'IDENTIFICADOR': ENTIDAD["idENTIDAD"]})
    if existe_SCHEMA and existe_ENTIDAD:
        result = await NOMBRE_COLLECTION_collection.update_one(
            {"IDENTIFICADOR": IDENTIFICADOR},
            {"$push": {"LISTA_ENTIDAD": ENTIDAD}},
        )
    return bool(result)

async def get_ENTIDAD_SCHEMA(IDENTIFICADOR: int):
    SCHEMA = await get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR)
    LISTA_ENTIDAD = []
    LISTA_ENTIDAD = SCHEMA["LISTA_ENTIDAD"]
    return LISTA_ENTIDAD

async def get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR: int, idENTIDAD: int):
    SCHEMA = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    for ENTIDAD in SCHEMA["LISTA_ENTIDAD"]:
        if ENTIDAD["idENTIDAD"] == idENTIDAD:
            return ENTIDAD
    return None

async def delete_ENTIDAD_SCHEMA(IDENTIFICADOR: int, idENTIDAD: int):
    SCHEMA = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    for ENTIDAD in SCHEMA["LISTA_ENTIDAD"]:
        if ENTIDAD["idENTIDAD"] == idENTIDAD:
            SCHEMA["LISTA_ENTIDAD"].remove(ENTIDAD)
            await update_SCHEMA(IDENTIFICADOR, SCHEMA)
            return True
    return False

async def update_ENTIDAD_SCHEMA(IDENTIFICADOR: int, ENTIDAD: dict):
    SCHEMA = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    for item in SCHEMA["LISTA_ENTIDAD"]:
        if item["idENTIDAD"] == ENTIDAD["idENTIDAD"]:
            item["CAMPO_ACTUALIZAR"] = ENTIDAD["CAMPO_ACTUALIZAR"]
            await update_SCHEMA(IDENTIFICADOR, SCHEMA)
            return True
    return False

"""

#LISTA CAMPO IDENTIFICADOR
"""
Usar cuando hay una lista que tiene referencias mediante ids


async def add_ENTIDAD_SCHEMA(IDENTIFICADOR: int,idENTIDAD: int):
    result = False
    existe_SCHEMA = await NOMBRE_COLLECTION_collection.find_one({'IDENTIFICADOR': IDENTIFICADOR})
    existe_ENTIDAD = await NOMBRE_COLLECTION_collection.find_one({'IDENTIFICADOR': idENTIDAD})
    if existe_SCHEMA and existe_ENTIDAD:
        result = await NOMBRE_COLLECTION_collection.update_one(
            {"IDENTIFICADOR": IDENTIFICADOR},
            {"$push": {"LISTA_ENTIDAD": idENTIDAD}},
        )
    return result

async def get_ENTIDAD_SCHEMA(IDENTIFICADOR: int):
    SCHEMA = await get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR)
    LISTA_ENTIDAD = []
    for idENTIDAD in SCHEMA["LISTA_ENTIDAD"]:
        #OPCION 1
        result = await get_SCHEMA_IDENTIFICADOR(idENTIDAD)
        LISTA_ENTIDAD.append(result)
        #OPCION 2
        LISTA_ENTIDAD.append(idENTIDAD)
    return LISTA_ENTIDAD

async def get_ENTIDAD_SCHEMA_idENTIDAD(IDENTIFICADOR: int, idENTIDAD: int):
    SCHEMA = await get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR)
    for id_item in SCHEMA["LISTA_ENTIDAD"]:
        if id_item == idENTIDAD:
            result = await get_SCHEMA_IDENTIFICADOR(idENTIDAD)
            return result
    return None

async def delete_ENTIDAD_SCHEMA(IDENTIFICADOR: int, idENTIDAD: int):
    SCHEMA = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    for id_item in SCHEMA["LISTA_ENTIDAD"]:
        if id_item == idENTIDAD:
            SCHEMA["LISTA_ENTIDAD"].remove(idENTIDAD)
            await update_SCHEMA(IDENTIFICADOR, SCHEMA)
            return True
    return False

"""