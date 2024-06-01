from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, RedirectResponse

from container import Container
from schemas.request import CreateShortModelDto
from schemas.response import ShortKeyDto, ShortCountDto
from services.url_service import ShortURLService

router = APIRouter()


@router.post("/shorten", response_model=ShortKeyDto)
@inject
def create_shorten_key(request: CreateShortModelDto,
                       short_service: ShortURLService = Depends(Provide[Container.short_service])):
    created_model = short_service.create_short_model(
        original_url=request.url,
        expire_time=request.expire_time,
    )

    dto = ShortKeyDto(
        shorten_key=created_model.shorten_key,
        expire_at=created_model.expire_at
    )
    response_json = jsonable_encoder(dto)
    return JSONResponse(content=response_json, status_code=status.HTTP_201_CREATED)


@router.get("/stats/{shorten_key}", response_model=ShortCountDto)
@inject
def status_short_key(shorten_key,
                     short_service: ShortURLService = Depends(Provide[Container.short_service])):
    try:
        short_obj = short_service.get_shorten_model(shorten_key)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    dto = ShortCountDto(
        shorten_key=short_obj.shorten_key,
        count=short_obj.count,
        expire_at=short_obj.expire_at
    )
    response_json = jsonable_encoder(dto)
    return JSONResponse(content=response_json, status_code=status.HTTP_200_OK)


@router.get("/{shorten_key}", responses={
    301: {"description": "redirect to original url"},
    404: {"description": "not found key"}
})
@inject
def redirect_to_origin(shorten_key,
                       short_service: ShortURLService = Depends(Provide[Container.short_service])):
    if original_url := short_service.get_original_url(shorten_key):
        return RedirectResponse(url=original_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        return JSONResponse(content={"message": "Not found key"}, status_code=status.HTTP_404_NOT_FOUND)
