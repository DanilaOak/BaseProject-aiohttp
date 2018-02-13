from aiohttp import web
from sqlalchemy import literal_column, select, exists

from app.models import get_model_by_name
from app.services.serializers import serialize_body


@serialize_body('user_schema')
async def create_user(request: web.Request, body) -> web.Response:
    user_table = get_model_by_name('user')
    exist = await request.app['pg'].fetchval(select([exists().where(user_table.c.login == body['login'])]))

    if exist:
        return web.Response(status=200, body='Not so fast m...f...')

    data = await request.app['pg'].fetchrow(user_table.insert().values(**body).returning(literal_column('*')))

    return web.Response(status=201, body=str(data))