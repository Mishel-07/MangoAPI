import httpx
from utils import BASE_URL, Chat

class Mango:
    """
    A class to generate content using AI models.
    """

    def __init__(self, base_url=BASE_URL, **kwargs):
        """
        Initialize the class with the base URL of the API.

        Args:
            base_url (str, optional): The base URL of the API. Defaults to "BASE_URL".
        """
        self.base_url = base_url   
        self.session = httpx.Client()
        self.chat = Chat(self)
        self.timeout = kwargs.get("timeout")
            
    def _do_request(self, endpoint, **kwargs):
        response = self.session(
            method=kwargs.get("method"),
            url=f"{self.base_url}/{endpoint}",
            timeout=self.timeout,
            json=kwargs.get("json"),
            params=kwargs.get("params"),
        ) 
        if response.status_code != 200:
        
                            
