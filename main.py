import os
import asyncio
import aiohttp_jinja2
import jinja2
from aiofauna import *
from aiohttp_sse import sse_response


FAUNA_SECRET = os.environ.get("FAUNA_SECRET")


@aiohttp_jinja2.template("index.j2")
async def index_handler(request: Request) -> Response:
    """Index handler."""

    return {"chart_type": "line"}

async def sse_handler(request: Request) -> Response:
    """SSE handler."""
    async with sse_response(request) as resp:  
        print(resp.headers)
        while True:
            _ = (await Client(os.environ.get(FAUNA_SECRET)).query(q.now()))["@ts"] # type: ignore
            await resp.send(_)
            await asyncio.sleep(1)
            
async def create_app():

    """Create application."""

    app = Application()

    # Add routes

    
    
    app.router.add_get("/", index_handler)

    app.router.add_get("/api/latency", sse_handler)
    
    app.router.add_static("/static", "static", show_index=True)
    
    jinja2_env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader("templates"),
        enable_async=True,
    )
    
    jinja2_env.variable_start_string = "@{"
    jinja2_env.variable_end_string = "}"
    
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, "localhost", 8080)
    await site.start()
    while True:
        await asyncio.sleep(1000)