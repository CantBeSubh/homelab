from fastmcp import FastMCP

proxy = FastMCP.as_proxy("https://mcp.homelab.subhranshu.com/mcp", name="Homelab Proxy")

if __name__ == "__main__":
    proxy.run()
