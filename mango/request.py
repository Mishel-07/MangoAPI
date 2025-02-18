import httpx
from utils import BASE_URL

class Request:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = httpx.Client()  
      
    def post(self, endpoint, json=None):
        if data:
            response = self.session.post(f"{self.base_url}/{endpoint}", json=data)  
            return response.json()
        else:
            response = self.session.post(f"{self.base_url}/{endpoint}")
        return response.json()
          
    def get(self, endpoint, params=None):
        if params:
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
        else:
            response = self.session.get(f"{self.base_url}/{endpoint}")
        return response.json()
