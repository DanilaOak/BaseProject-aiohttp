from aiohttp import web

from app.models import get_model_by_name
from app.services.serializers import serialize_body


@serialize_body('user_schema')
async def create_user(request: web.Request, body) -> web.Response:
    user_table = get_model_by_name('user')
    data = await request.app['pg'].fetchrow(user_table.insert().values(**body).returning(literal_column('*')))

    return web.json_response(status=201, data=data)