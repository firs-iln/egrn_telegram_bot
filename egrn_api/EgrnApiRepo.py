import pprint
from typing import Optional, Literal
import httpx


from .types import SearchResponse, CreateRequestResponse, CheckRequestResponse, DownloadOrderResponse


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
            response.raise_for_status()
            return response.json()

    async def _get(self, url: str, params: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + url, params=params | self.params,
                                        headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def _get_file(self, url: str, params: dict) -> (bytes, str):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + url, params=params | self.params,
                                        headers=self.headers)

            response.raise_for_status()

            pprint.pprint(response.headers)

            filename = response.headers["content-disposition"].split('filename=')[-1]

            return response.content, filename

    async def search_cadastral_full(self, cadnum: str) -> Optional[SearchResponse]:
        url = "search/cadastrFull"
        data = {"cad_num": cadnum}

        response = await self._post(url, data)

        if response["query"] != "success" or response["found"] == 0:
            return None

        return SearchResponse(**response)

    async def create_order(self, cadnum: str, order_type: int = 1) -> CreateRequestResponse:
        url = "order/create"
        data = {
            "cad_num": cadnum,
            "order_type": order_type,
        }

        response = await self._post(url, data)

        return CreateRequestResponse(**response)

    async def check_order(self, order_id: str) -> Optional[CheckRequestResponse]:
        url = "order/check"
        data = {
            "order_id": order_id,
        }

        response = await self._post(url, data)

        data = response.get("info", [])
        if not data:
            return None

        data = data[0]

        return CheckRequestResponse.model_validate(data)

    async def download_order_file(self, order_id: str, file_type: Literal['pdf', 'pdf-report', 'json', 'zip'] = 'pdf')\
            -> DownloadOrderResponse:
        """
        Returns file bytes and file extension (pdf, json, zip). pdf-report file_type has pdf extension.

        Args:
            order_id:
            file_type:

        Returns:
            file_bytes:
            file_extension:
        """

        url = "order/download"
        params = {
            "order_id": order_id,
            "format": file_type,
        }

        file_bytes, filename = await self._get_file(url, params)

        return DownloadOrderResponse(
            file_bytes=file_bytes,
            filename=filename,
        )
