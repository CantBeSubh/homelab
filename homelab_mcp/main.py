from fastmcp import FastMCP
from servers import resume_mcp
import asyncio

main_mcp = FastMCP(name="homelab")

async def setup():
    await main_mcp.import_server("resume", resume_mcp)

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run()