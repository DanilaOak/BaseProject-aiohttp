from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from core.app import create_app

class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        
        return create_app()

    @unittest_run_loop
    async def test_version(self):
        request = await self.client.request("GET", "/api/version")
        assert request.status == 200
        text = await request.json() 
        assert 'version' in text