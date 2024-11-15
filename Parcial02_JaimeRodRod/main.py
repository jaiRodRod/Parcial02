import json
from fastapi import FastAPI
from routers import colaborador_router, tarea_router
urls = json.load(open('urls.json'))

"""
CTRL-F A CAMBIAR:
    - ROUTER
    - SCHEMA_URL
"""

"""
For requirements do:
    - pip freeze > requirements.txt
"""

app = FastAPI()
app.include_router(colaborador_router.router,prefix=urls["colaborador_url"])
app.include_router(tarea_router.router,prefix=urls["tarea_url"])