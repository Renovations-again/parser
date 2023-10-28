import uvicorn

from fastapi import FastAPI

from api.routers import main_router
from core.config import settings

app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)