from fastmcp import FastMCP
from servers import resume_mcp
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import asyncio
import uvicorn

main_mcp = FastMCP(name="homelab")

@main_mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

custom_middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"]),
]

http_app = main_mcp.http_app(middleware=custom_middleware)

async def setup():
    await main_mcp.import_server("resume", resume_mcp)

if __name__ == "__main__":
    asyncio.run(setup())
    uvicorn.run(http_app, host="0.0.0.0", port=4200)
