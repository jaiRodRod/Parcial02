import json
from fastapi import FastAPI
from routers import ROUTER
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
app.include_router(ROUTER.router,prefix=urls["SCHEMA_URL"])