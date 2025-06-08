from fastmcp import FastMCP

# Create a proxy to a remote server
proxy = FastMCP.as_proxy(
    "http://192.168.1.25:4200/mcp", 
    name="Homelab Proxy"
)

if __name__ == "__main__":
    proxy.run() 