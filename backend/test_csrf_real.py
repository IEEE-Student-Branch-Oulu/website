import asyncio

from httpx import ASGITransport, AsyncClient

from app.auth.sessions import COOKIE_NAME as SESSION_COOKIE
from app.main import create_app


async def main():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/members/", cookies={SESSION_COOKIE: "fake"}, json={"name": "test"}
        )
        print("Status code:", resp.status_code)


asyncio.run(main())
