import httpx

from .chat import Chat

class Mango:
    """
    A class to generate content using AI models.
    """

    def __init__(self, base_url="https://mangooapi.onrender.com", **kwargs):
        """
        Initialize the class with the base URL of the API.

        Args:
            base_url (str, optional): The base URL of the API. Defaults to "BASE_URL".
        """
        self.base_url = base_url   
        self.session = httpx.Client()
        self.chat = Chat(self)
        self.api_key = kwargs.get("api_key") # Now, I'll make it free, so maybe in the future, it will be required to include an API key 🥭
        self.timeout = kwargs.get("timeout")
            
    def _do_request(self, endpoint: str, **kwargs):
        response = self.session.request(
            method=kwargs.get("method"),
            url=f"{self.base_url}/{endpoint}",
            timeout=self.timeout,
            json=kwargs.get("json"),
            params=kwargs.get("params"),
        ) 
        if response.status_code != 200:
            raise Exception(f"Error: Report https://github.com/Mishel-07/MangoAPI/issues")
        else:
            return response.json()
            
    def PostCompletion(self, input: str):
        try:
            response = self._do_request("mango", json={"model": "gpt-3.5-turbo", messages: [{"role": "user", "content": input}]})
            return response 
        except:
            raise Exception(f"Error: Report https://github.com/Mishel-07/MangoAPI/issues")
                                
