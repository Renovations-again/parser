# import uvicorn

import asyncio
from fastapi import FastAPI

from api.routers import main_router
from core.config import settings
from db.orm import insert_data
from db.t import insert_data_vodopad


app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(main_router)

if __name__ == '__main__':
    # uvicorn.run('main:app', reload=True)
    # asyncio.run(insert_data())
    asyncio.run(insert_data_vodopad())
