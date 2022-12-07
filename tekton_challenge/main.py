import pathlib

import uvicorn
from fastapi import FastAPI

from tekton_challenge.container import Container
from tekton_challenge.routers import inventory_router


def create_app() -> FastAPI:
    """ Generate the FastAPI app"""
    container = Container()

    db = container.db()
    db.create_database()

    # Init WSGI app
    application = FastAPI()
    application.container = container

    # Routers
    application.include_router(inventory_router)

    @application.get("/")
    def read_root():
        return {"Hello": "World"}

    return application


app = create_app()

if __name__ == "__main__":
    cwd = pathlib.Path(__file__).parent.resolve()
    uvicorn.run("tekton_challenge.main:app", host="0.0.0.0", port=8000, reload=True, log_config=f"{cwd}/log.ini")
