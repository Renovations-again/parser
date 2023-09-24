from fastapi import APIRouter

from api.endpoints import petrovich_api_router, vodopad_api_router

main_router = APIRouter()
main_router.include_router(
    petrovich_api_router, prefix='/petrovich', tags=['Петрович']
)
main_router.include_router(
    vodopad_api_router, prefix='/vodopad', tags=['Водопад']
)
