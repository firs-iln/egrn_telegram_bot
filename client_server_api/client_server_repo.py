import httpx
import random


class ClientServerAPI:
    def __init__(self, host: str):
        self.host = host
        self.base_url = f"http://{host}/api/v1/order"

    async def post_request(self, request_data: dict) -> dict:
        url = "/"
        return {"id": random.randint(1, 10000)}

    async def get_request(self, request_id: int):
        with open('test.xlsx', 'rb') as file:
            return file.read()
