import os
from typing import Optional

import httpx
from fastmcp import FastMCP

homeassistant_mcp = FastMCP("homeassistant")


@homeassistant_mcp.tool
async def get_entities(component: Optional[str]) -> str:
    """
    Get All Entities in my Homelab for a given component. If no component is specified, returns all entities.

    Args:
        component (Optional[str]): The component to filter entities by. If None, returns all entities. Eg: 'light', 'sensor', etc.
    Returns:
        str[]: A list of entity IDs as strings.
    """
    url = "http://192.168.1.25:8123/api/states"

    headers = {
        "Authorization": f"Bearer ${os.getenv('HA_TOKEN')}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if component:
                return [
                    entity["entity_id"]
                    for entity in data
                    if entity["entity_id"].startswith(f"${component}.")
                ]

            return [entity["entity_id"] for entity in data]
        except Exception:
            return None
