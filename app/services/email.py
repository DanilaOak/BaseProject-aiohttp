import json

from aiohttp import ClientSession, web


async def send_email(scheme: str, host: str, data: dict):
    async with ClientSession() as session:
        async with session.post(f'{scheme}://{host}/api/v1/emails', json=data) as resp:
            body = await resp.json()
            return body
