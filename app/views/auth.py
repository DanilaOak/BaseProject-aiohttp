import json
from datetime import datetime, timedelta

from aiohttp import web
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from aiohttp_swagger import *
from sqlalchemy import and_

from app.models import get_model_by_name, row_to_dict
from app.services.serializers import serialize_body
from app.services.email import send_email
from app.services.auth import set_authorization_coockie

auth_routes = web.RouteTableDef()

@swagger_path('swagger/login.yaml')
@auth_routes.post('/api/v1/auth/login')
@serialize_body('login_schema', custom_exc=web.HTTPUnauthorized)
async def login(request: web.Request, body) -> web.Response:
    user_table = get_model_by_name('user')

    user = await request.app['pg'].fetchrow(user_table.select().where(user_table.c.login == body['login']))

    if not user:
        raise web.HTTPUnauthorized(body=json.dumps({'error': 'Invalid username / password combination'}),
                                   content_type='application/json')

    if body['password'] == user['password']:
        return await set_authorization_coockie(user, {'hours': 24}, request.app['config']['SECRET_KEY'])

    raise web.HTTPUnauthorized(
        body=json.dumps({'error': 'Invalid username / password combination'}), content_type='application/json')

@swagger_path('swagger/logout.yaml')
@auth_routes.get('/api/v1/auth/logout')
async def logout(request: web.Request) -> web.Response:
    response = web.json_response({'status': 'Ok'})
    response.del_cookie(name='AppCoockie')
    return response


@auth_routes.post('/api/v1/restorepassword')
@serialize_body('forgot_password')
async def forgot_password(request: web.Request, body) -> web.Response:
    # check is user exist
    user_table = get_model_by_name('user')
    user = await request.app['pg'].fetchrow(user_table.select().where(
        and_(user_table.c.login == body['login'], user_table.c.email == body['email'])))
    
    if not user: 
        raise web.HTTPNotFound(content_type='application/json', body=json.dumps({'error': f'User not found'}))
    # generate token
    expiration_time = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode(payload={'login': user['login'],
                                'user_id': user['user_id'],
                                'exp': expiration_time},
                       key=request.app['config']['RESTORE_EMAIL_KEY']).decode('utf-8')
    # generate url
    url = '{scheme}://{host}/api/v1/restorepassword/{token}'.format(scheme=request.scheme,
                                                                    host=request.app['config']['HOST'],
                                                                    token=token)
    # sent email with url
    email_resp = await send_email(request.scheme, request.app['config']['EMAIL_SERVICE_HOST'], data={'email_type': 'restore_password',
                                                                                                     'to_name': user['login'],
                                                                                                     'to_addr': user['email'],
                                                                                                     'linc': url,
                                                                                                     'subject': 'Restore Password'})

    if not email_resp['success']:
        raise web.HTTPUnprocessableEntity(content_type='application/json', body=json.dumps({'email_service_error': email_resp['error']}))
    
    return web.Response(status=200, content_type='application/json', body=json.dumps({'status': 'Ok'}))


@auth_routes.get('/api/v1/restorepassword/{token}')
async def restore_password_confirmation(request: web.Request) -> web.Response:
    token = request.match_info['token']

    try:
        user = jwt.decode(token, key=request.app['config']['RESTORE_EMAIL_KEY'])
    except ExpiredSignatureError:
        raise web.HTTPUnauthorized(body=json.dumps({'error': 'Token expired'}),
                                    content_type='application/json')
    except DecodeError:
        raise web.HTTPUnauthorized(body=json.dumps({'error': 'Invalid token'}),
                                    content_type='application/json')

    return await set_authorization_coockie(user, {'minutes': 5}, request.app['config']['SECRET_KEY'])
