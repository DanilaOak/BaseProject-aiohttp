from aiohttp import web
from aiohttp_swagger import *

from app.models import get_model_by_name


@swagger_path("swagger/api_version.yaml")
async def get_version(request: web.Request):
    return web.json_response(data={'version': request.app['config']['VERSION']})

async def get_db_version(request: web.Request):
    table = get_model_by_name('system_settings')
    db_version = await request.app['pg'].fetchval()
    return web.json_response(data={'db_version': None})