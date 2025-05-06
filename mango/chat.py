class Chat:
    def __init__(self, mango, **kwargs):
        self.mango = mango
        self.completions = Completions(self)

class Completions:
    def __init__(self, chat, **kwargs):
        self.chat = chat

    def create(self, model: str = None, messages: list = None, **kwargs):                          
        if not model:
            raise ValueError("model is required , You can see model here https://www.api.mangoi.in/v1/models")
        if not messages:
            raise ValueError("messages is required")                       
        try:
            response = self.chat.mango._do_request("v1/chat/completions", json={'messages': messages, 'model': model}, method="POST")   
            if response.get("status") == "error":
                raise Exception(f"Error: Report https://github.com/Mishel-07/MangoAPI/issues")
            if response.get("response") == "invalid model":
                raise ValueError("Invalid model")                        
            return Choices(response)
        except:
            raise Exception(f"Error: Report https://github.com/Mishel-07/MangoAPI/issues")
            
class Choices:
    def __init__(self, response, **kwargs):    
        self.status = response.get("response", None)
        self.object = response.get("object", None)
        self.response = response.get("response", None)
        self.choices = [Messages(msg) for msg in response.get("choices", [])]
        
    def __repr__(self):
        return str(self.__dict__)  

class Messages:
    def __init__(self, json, **kwargs):
        self.message = Response(json["message"])
        
    def __repr__(self):
        return str(self.__dict__)  
        
class Response:
    def __init__(self, chat, **kwargs):
        self.role = chat["role"]
        self.content = chat["content"]

    def __repr__(self):
        return str(self.__dict__)  
      
