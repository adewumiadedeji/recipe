import httpx
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class ServiceClient:
    def __init__(self, base_url: str, service_name: str):
        self.base_url = base_url
        self.service_name = service_name
        self.client = httpx.AsyncClient(base_url=base_url)

    async def request(self, method: str, endpoint: str, **kwargs):
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error communicating with {self.service_name}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Error communicating with {self.service_name}")
