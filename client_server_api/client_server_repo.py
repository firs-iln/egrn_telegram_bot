import httpx
import random


class ClientServerAPI:
    def __init__(self, host: str):
        self.host = host
        self.base_url = f"http://{host}/api/v1/order"

    async def post_request(self, order_id: str, reason: str, **kwargs) -> dict:
        if not kwargs:
            kwargs = dict()
        async with httpx.AsyncClient(follow_redirects=True) as client:
            print(kwargs)
            response = await client.post(self.base_url + f"/{order_id}/callback/{reason}/", json=kwargs)
            response.raise_for_status()
            return response.json()

    async def get_request(self, order_id: int, reason: str = 'fioFile') -> dict:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(self.base_url + f"/{order_id}/{reason}/")
            response.raise_for_status()
            return response.json()

    async def get_fio_file(self, order_id: int) -> bytes:
        url = self.base_url + f"/{order_id}/fioFile/"
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
        return response.content
