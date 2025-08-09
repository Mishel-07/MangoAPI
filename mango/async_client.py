import httpx
import os
from .async_chat import AsyncChat
from .async_client import AsyncImages
from .errors import (
    APIKeyMissingError,
    WordMissingError,
    TimeoutMangoError,
    ConnectionMangoError,
    ResponseMangoError,
    RateLimitError,
    AuthenticationError,
    ModelNotFoundError,
    ServerBusyError,
    ServerError,
)
from .types import WordResult

class AsyncMango:
    """
    Asynchronous Mango API client to access moderation and chat tools.
    """

    def __init__(self, api_key: str = None, base_url: str = "https://api.mangoi.in/v1", timeout: float = 10):
        """
        Initialize the asynchronous Mango client.

        Args:
            api_key (str, optional): Your Mango API key. Defaults to os.getenv("MANGO_API_KEY").
            base_url (str, optional): Base URL of the API. Defaults to Mango's v1 endpoint.
            timeout (float, optional): Request timeout. Defaults to 10 seconds.
        """
        self.api_key = api_key or os.getenv("MANGO_API_KEY")
        self.base_url = base_url
        self.timeout = timeout
        self.session = httpx.AsyncClient()
        self.chat = AsyncChat(self)
        self.images = AsyncImages(self)

    async def __aenter__(self):
        """Enter the async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Exit the async context manager, closing the HTTP session."""
        await self.session.aclose()

    async def _do_request(self, endpoint: str, method: str = "GET", json: dict = None, headers: dict = None):
        """
        Internal method to make asynchronous HTTP requests.

        Args:
            endpoint (str): API endpoint to call.
            method (str): HTTP method (e.g., GET, POST).
            json (dict, optional): JSON payload for the request.
            headers (dict, optional): Additional headers.

        Returns:
            Response data or raises an error based on the API response.
        """
        if not self.api_key:
            raise APIKeyMissingError()

        url = f"{self.base_url}/{endpoint}"

        try:
            response = await self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                json=json,
                headers=headers
            )
        except httpx.ConnectError:
            raise ConnectionMangoError()
        except httpx.TimeoutException:
            raise TimeoutMangoError()

        try:
            data = response.json()
        except Exception:
            raise ResponseMangoError(status_code=response.status_code, message=response.text)

        if isinstance(data, dict) and "error" in data:
            err = data["error"]
            err_type = err.get("type", "").lower()
            err_msg = err.get("message", "Unknown error from API.")

            if err_type == "rate_limit_error":
                raise RateLimitError(err_msg)
            elif err_type == "authentication_error":
                raise AuthenticationError(err_msg)
            elif err.get("code") == "model_not_found":
                raise ModelNotFoundError(err.get("param", "unknown"))
            elif err.get("code") == "server_busy":
                raise ServerBusyError()
            elif err.get("code") == "internal_error":
                raise ServerError()
            else:
                raise ResponseMangoError(status_code=response.status_code, message=err_msg)

        if response.status_code != 200:
            raise ResponseMangoError(status_code=response.status_code, message=str(data))

        if json and json.get("stream"):
            return response.text

        return data

    async def words(self, word: str, accurate: int = 85) -> WordResult:
        """
        Asynchronously analyze a word using Mango's moderation model.

        Args:
            word (str): Word to check.
            accurate (int, optional): Accuracy level (default: 85).

        Returns:
            WordResult: Structured result object.
        """
        if not word:
            raise WordMissingError()

        endpoint = f"words/{word}/api_key={self.api_key}/accurate={accurate}"
        data = await self._do_request(endpoint)
        return WordResult.from_json(data)
