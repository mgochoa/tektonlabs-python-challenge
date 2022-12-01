from fastapi import FastAPI

from tekton_challenge.config.database import create_tables
from tekton_challenge.routers import inventory_router

# Database init
create_tables()

# Init WSGI app
app = FastAPI()

# Routers
app.include_router(inventory_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
