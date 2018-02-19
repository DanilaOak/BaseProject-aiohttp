from aiohttp import web
from aiohttp_swagger import *
from aiohttp_security import (
    remember, forget, authorized_userid,
    has_permission, login_required,
)

from app.models import get_model_by_name


@swagger_path('swagger/api_version.yaml')
async def get_version(request: web.Request):
    
    username = await authorized_userid(request)
    import ipdb; ipdb.set_trace()
    print(username)
    return web.json_response(data={'version': request.app['config']['VERSION']})
