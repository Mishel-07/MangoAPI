BASE_URL = "https://mangooapi.onrender.com/mango"

class Chat:
    def __init__(self, mango, **kwargs):
        self.mango = mango
        self.completions = Completions(self)

class Completions:
    def __init__(self, chat, **kwargs):
        self.chat = chat

    def create(self, model=None, messages=None, **kwargs):                          
        if not model:
            raise ValueError("model os required , You can see model here https://mangooapi.onrender.com/models")
        if not messages:
            raise ValueError("An error Report @XBOTSUPPORTS or https://github.com/Mishel-07/MangoAPI/issues")
        ms = {'messages': messages}        
        api = f"{self.chat.mango.base_url}?model={model}"  
        response = self.chat.mango.session.post(api, json=ms)
        k = response.json()
        if "messages" in k and "invalid model" in k["messages"]:
            raise ValueError("Invalid model")
        if response.status_code == 200:         
            return Choices(response.json())
        else:
            raise Exception(f"Error: Report  @XBOTSUPPORTS or https://github.com/Mishel-07/MangoAPI/issues")

class Choices:
    def __init__(self, response, **kwargs):          
        self.response = Response(self["response"])

  class Response:
    def __init__(self, chat, **kwargs):
        self.content = Response(["content"])
      
