import json

from aiohttp import web

from app.services.serializers import InvalidParameterException

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPNotFound as exc:
        raise web.HTTPNotFound(body=json.dumps({'error': str(exc)}), content_type='application/json')
    except InvalidParameterException as exc:
        raise web.HTTPUnprocessableEntity(body=json.dumps({'error': str(exc)}),
                                          content_type='application/json')
