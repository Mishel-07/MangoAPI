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
            raise ValueError("model is required , You can see model here https://mangooapi.onrender.com/models")
        if not messages:
            raise ValueError("messages is required")
        ms = {'messages': messages, 'model': model}                
        try:
            response = self.chat.mango._do_request("mango", json=ms, method="POST")
            k = response.json()
            if "messages" in k and "invalid model" in k["messages"]:
                raise ValueError("Invalid model")                        
            return Choices(response)
        except:
            raise Exception(f"Error: Report https://github.com/Mishel-07/MangoAPI/issues")
            
class Choices:
    def __init__(self, response, **kwargs):          
        self.response = Response(self["response"])

  class Response:
    def __init__(self, chat, **kwargs):
        self.content = Response(["content"])
      
