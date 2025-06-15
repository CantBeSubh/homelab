import logging
import os
from enum import Enum
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

logger = logging.getLogger(__name__)

homeassistant_mcp = FastMCP("homeassistant")


class ServiceEnum(str, Enum):
    TURN_ON = "turn_on"
    TURN_OFF = "turn_off"
    TOGGLE = "toggle"


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
        "Authorization": f"Bearer {os.getenv('HA_TOKEN')}",
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
                    if entity["entity_id"].startswith(f"{component}.")
                ]

            return [entity["entity_id"] for entity in data]
        except Exception:
            logger.error(
                f"Error fetching entities from Home Assistant API: {url}: {response.status_code}|> \n {response.text}"
            )
            return None


@homeassistant_mcp.tool
async def set_entity(entity_id: str, service: str, data: dict) -> str:
    """
    Set the state of an entity in Home Assistant.

    `data` could have the following keys:
        - brightness: int
        - color_temp_kelvin: int
        - rgb_color: list[int] (size 3, values between 0 and 255)

    Example:
        await set_entity("light.living_room", "turn_on", {"brightness": 255})

    Args:
        entity_id (str): The entity ID to set the state of.
        service (str): The service to call on the entity. One of these three - "turn_on", "turn_off", "toggle".
        data (dict): The data to pass to the service.
    Returns:
        str: The response from the service call.
    """
    url = f"http://192.168.1.25:8123/api/services/homeassistant/{service}"
    payload = {
        "entity_id": entity_id,
        **data,
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('HA_TOKEN')}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return "OK"
        except Exception as e:
            logger.exception(
                f"Exception occurred while setting state for entity {entity_id} with service {service}: {e}"
            )
            logger.error(
                f"Error setting state for entity {entity_id} with service {service}: {url}: {response.status_code}|> \n {response.text}"
            )
            return "ERROR"
