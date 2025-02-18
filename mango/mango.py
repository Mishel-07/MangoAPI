import httpx

class Mango:
    """
    A class to generate content using AI models.
    """

    def __init__(self, base_url="https://horrid-api.vercel.app/mango", **kwargs):
        """
        Initialize the class with the base URL of the API.

        Args:
            base_url (str, optional): The base URL of the API. Defaults to "https://horridapi.onrender.com/mango".
        """
        self.base_url = base_url   
        self.session = httpx.Client()
        self.chat = Chat(self)
                            
