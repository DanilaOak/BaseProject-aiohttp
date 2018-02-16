import json

from aiohttp import web
from sqlalchemy import literal_column, select, exists

from app.models import get_model_by_name
from app.services.serializers import serialize_body


@serialize_body('user_schema')
async def create_user(request: web.Request, body) -> web.Response:
    user_table = get_model_by_name('user')
    login = body['login']
    exist = await request.app['pg'].fetchval(select([exists().where(user_table.c.login == login)]))

    if exist:
        return web.HTTPConflict(body=json.dumps({'error': f'User with login "{login}" already exist'}), content_type='application/json')

    data = await request.app['pg'].fetchrow(user_table.insert().values(**body).returning(literal_column('*')))
    body['id'] = data['id']
    del body['password']

    return web.Response(status=201, content_type='application/json', body=json.dumps(body))