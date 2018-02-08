from aiohttp import web

from .routes import setup_routes
from .utils import get_config


def create_app():
    app = web.Application()
    app['config'] = get_config()
    setup_routes(app)

    return app
