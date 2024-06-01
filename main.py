from fastapi import FastAPI
from starlette.responses import JSONResponse

from api import short
from container import Container
from tasks import hard_delete_expired_keys, soft_delete_expired_keys


def create_app():
    container = Container()
    db = container.db()
    db.create_database()
    _app = FastAPI()
    _app.container = container
    _app.include_router(short.router, prefix="/api")
    return _app


app = create_app()


@app.on_event("startup")
def startup_event():
    hard_delete_expired_keys.delay()
    soft_delete_expired_keys.delay()


@app.get("/original-site")
def original_site():
    return JSONResponse("Hello World", status_code=200)
