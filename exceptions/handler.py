from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from main import app


class ErrorResponseModel(BaseModel):
    detail: str


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(detail=exc.detail).dict()
    )


@app.exception_handler(Exception)
def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponseModel(detail={"detail": "Internal server error"}).dict()
    )
