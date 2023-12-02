from typing import Optional
import httpx


from .types import SearchResponse


class EGRNAPI:
    BASE_URL = "https://reestr-api.ru/v1/"

    def __init__(self, auth_token: str):
        self.base_url = self.BASE_URL
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.params = {"auth_token": auth_token}

    async def _post(self, url: str, data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url + url, params=self.params, data=data,
                                         headers=self.headers)
            return response.json()

    async def _get(self, url: str, params: dict) -> dict:
        async with httpx.Client() as client:
            response = await client.get(self.base_url + url, params=params,
                                        headers=self.headers)
            return response.json()

    async def search_cadastral_full(self, cadnum: str) -> Optional[SearchResponse]:
        url = "search/cadastrFull"
        data = {"cad_num": cadnum}

        response = await self._post(url, data)

        if response["query"] != "success" or response["found"] == 0:
            return None

        return SearchResponse(**response)
