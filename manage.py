import argparse
import asyncio

from aiohttp import web

from core.app import create_app


app = create_app()
web.run_app(app, host='127.0.0.1', port=8080)
