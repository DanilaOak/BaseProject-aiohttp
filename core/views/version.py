from aiohttp import web


async def get_version(request: web.Request):
    return web.json_response(data={'version': request.app['config']['VERSION']}, status=200)