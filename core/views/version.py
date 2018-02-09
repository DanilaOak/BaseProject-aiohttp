from aiohttp import web


async def get_version(request: web.Request):
    return web.json_response(data={'version': request.app['config']['VERSION']})

async def get_db_version(request: web.Request):
    db_version = await request.app['pg'].fetchval()
    return web.json_response(data={'db_version': None})