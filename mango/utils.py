BASE_URL = "https://mangooapi.onrender.com"

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
        try:
            response = self.chat.mango._do_request("mango", json={'messages': messages, 'model': model}, method="POST")           
            if "messages" in response and "invalid model" in response["messages"]:
                raise ValueError("Invalid model")                        
            return Choices(response)
        except:
            raise Exception(f"Error: Report https://github.com/Mishel-07/MangoAPI/issues")
            
class Choices:
    def __init__(self, response, **kwargs):    
        self.status = response["response"]
        self.object = response["object"]
        self.message= response["message"]
        self.choices = [Response(msg) for msg in response["choices"]]

class Response:
    def __init__(self, chat, **kwargs):
        self.role = content["role"]
        self.content = Response(["content"])
      
