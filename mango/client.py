import httpx
from .chat import Chat
from .errors import (
    APIKeyMissingError,
    WordMissingError,
    TimeoutMangoError,
    ConnectionMangoError,
    ResponseMangoError,
)
from .types import WordResult


class Mango:
    """
    Mango API client to access moderation and chat tools.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.mangoi.in/v1", timeout: float = 10.0):
        """
        Initialize the Mango client.

        Args:
            api_key (str): Your Mango API key.
            base_url (str, optional): Base URL of the API. Defaults to Mango's v1 endpoint.
            timeout (float, optional): Request timeout. Defaults to 10 seconds.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.session = httpx.Client()
        self.chat = Chat(self)

    def _do_request(self, endpoint: str, method: str = "GET", json: dict = None) -> dict:
        """
        Internal method to make HTTP requests.

        Args:
            endpoint (str): API endpoint with full query path.
            method (str): HTTP method, e.g., GET or POST.
            json (dict, optional): Optional JSON body for POST.

        Returns:
            dict: Parsed JSON response.

        Raises:
            MangoError subclasses depending on failure type.
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                json=json
            )
        except httpx.ConnectError:
            raise ConnectionMangoError()
        except httpx.TimeoutException:
            raise TimeoutMangoError()

        if response.status_code != 200:
            return response.text

        return response.json()

    def words(self, word: str, accurate: int = 85) -> WordResult:
        """
        Analyze a word using Mango's moderation model.

        Args:
            word (str): Word to check.
            accurate (int, optional): Accuracy level (default: 85).

        Returns:
            WordResult: Structured result object.

        Example:
            >>> client = Mango(api_key="your_api_key")
            >>> result = client.words("shit")
            >>> result.nosafe  # True
        """
        if not self.api_key:
            raise APIKeyMissingError()
        if not word:
            raise WordMissingError()

        endpoint = f"words/{word}/api_key={self.api_key}/accurate={accurate}"
        data = self._do_request(endpoint)
        return WordResult.from_json(data)
