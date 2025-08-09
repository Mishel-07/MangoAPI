from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class Choices:
    id: str
    created: int
    model: str
    index: int
    finish_reason: str
    status: str
    object: str
    usage: 'Usages'
    choices: List['Messages']

    def __init__(self, response):
        self.id = response.get("id")
        self.created = response.get("created")
        self.model = response.get("model")
        self.index = response.get("index")
        self.finish_reason = response.get("finish_reason")
        self.status = response.get("response")
        self.object = response.get("object")
        self.usage = Usages(response.get("usage", {}))
        self.choices = [Messages(msg) for msg in response.get("choices", [])]

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class Messages:
    message: 'Response'

    def __init__(self, json):
        self.message = Response(json["message"])

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class Response:
    role: str
    content: str
    tool_calls: List['ToolCall']

    def __init__(self, chat):
        self.role = chat.get("role")
        self.content = chat.get("content")
        self.tool_calls = [ToolCall(tc) for tc in chat.get("tool_calls", [])]

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class Usages:
    completion_tokens: int
    prompt_tokens: int

    def __init__(self, usage):
        self.completion_tokens = usage.get("completion_tokens")
        self.prompt_tokens = usage.get("prompt_tokens")

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class StreamingChoices:
    id: str
    object: str
    created: int
    model: str
    choices: List['StreamingMessages']

    def __init__(self, json):
        self.id = json.get("id")
        self.object = json.get("object")
        self.created = json.get("created")
        self.model = json.get("model")
        self.choices = [StreamingMessages(msg) for msg in json.get("choices", [])]

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class StreamingMessages:
    delta: 'StreamingResponse'
    index: int
    finish_reason: str

    def __init__(self, msg):
        self.delta = StreamingResponse(msg.get("delta", {}))
        self.index = msg.get("index")
        self.finish_reason = msg.get("finish_reason")

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class StreamingResponse:
    role: str
    content: str

    def __init__(self, data):
        self.role = data.get("role")
        self.content = data.get("content")

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class ToolFunction:
    name: str
    arguments: dict

    def __init__(self, data):
        self.name = data.get("name")
        self.arguments = data.get("arguments")

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class ToolCall:
    id: str
    index: int
    finish_reason: str
    type: str
    function: 'ToolFunction'

    def __init__(self, data):
        self.id = data.get("id")
        self.index = data.get("index")
        self.finish_reason = data.get("finish_reason")
        self.type = data.get("type")
        self.function = ToolFunction(data.get("function", {}))

    def __repr__(self):
        return str(self.__dict__)

@dataclass
class ImageResponse:
    created: int
    data: List['Image']

    def __init__(self, response):
        self.created = response.get("created")
        self.data = [Image(url=img.get("url")) for img in response.get("data", [])]

    def __repr__(self):
        return str([image.url for image in self.data])

@dataclass
class Image:
    url: str

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return self.url
        
class WordResult:
    """
    Represents the result of a word analysis using Mango's moderation API.

    Attributes:
        word (str): The word that was analyzed.
        content (str): The content category returned (e.g., "BAD_WORDS").
        nosafe (bool): Whether the word is considered unsafe.
    """

    def __init__(self, word: str, content: str, nosafe: bool):
        self.word = word
        self.content = content
        self.nosafe = nosafe

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "WordResult":
        """
        Creates a WordResult instance from a dictionary (JSON response).

        Args:
            data (dict): The JSON dictionary returned by the API.

        Returns:
            WordResult: The parsed result object.
        """
        return cls(
            word=data.get("word"),
            content=data.get("content"),
            nosafe=data.get("nosafe", False)
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the WordResult instance to a dictionary.

        Returns:
            dict: Dictionary representation of the result.
        """
        return {
            "word": self.word,
            "content": self.content,
            "nosafe": self.nosafe
        }

    def __repr__(self) -> str:
        return f"<WordResult word={self.word!r} content={self.content!r} nosafe={self.nosafe}>"
