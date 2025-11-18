from __future__ import annotations

from fastapi import APIRouter, FastAPI

from app.routers import scenes, titles


api = APIRouter()
api.include_router(scenes.router, prefix='/scenes', tags=['scenes'])
api.include_router(titles.router, prefix='/titles', tags=['titles'])

app = FastAPI(
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)
app.include_router(api, prefix='/api')
