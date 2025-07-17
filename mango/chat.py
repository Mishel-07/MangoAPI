import json
import io

from .errors import (
    MangoError,
    ModelRequiredError,
    MessagesRequiredError,
    ModelNotFoundError,
    ServerBusyError,
    ServerError,
    ConnectionMangoError,
    TimeoutMangoError,
    ResponseMangoError,
    RateLimitError,
    AuthenticationError
)


class Chat:
    """
    Chat is the main entry for accessing chat completions.

    Args:
        mango (object): The Mango API client instance.
    """

    def __init__(self, mango, **kwargs):
        self.mango = mango
        self.completions = Completions(self)


class Completions:
    """
    Provides access to chat completion endpoints.

    Args:
        chat (Chat): Parent Chat instance.
    """

    def __init__(self, chat, **kwargs):
        self.chat = chat

    def create(self, model: str = None, messages: list = None, tools: list = None, stream: bool = False, **kwargs):
        """
        Creates a chat completion.

        Args:
            model (str): The model ID to use.
            messages (list): A list of message objects (dicts).
            tools (list, optional): Tool definitions.
            stream (bool): Whether to stream the response.
            **kwargs: Additional request arguments.

        Raises:
            ModelRequiredError: If model is not provided.
            MessagesRequiredError: If messages are not provided.
            ModelNotFoundError: If the model is not found.
            ServerBusyError: If the server is overloaded.
            ServerError: For unknown internal errors.
            ConnectionMangoError: If connection fails.
            TimeoutMangoError: If request times out.
            ResponseMangoError: For unexpected responses.

        Returns:
            Choices | Generator: Parsed response or streaming chunks.
        """
        if not model:
            raise ModelRequiredError()
        if not messages:
            raise MessagesRequiredError()

        payload = {
            "model": model,
            "messages": messages,
            "tools": tools,
            "stream": stream
        }

        try:
            response = self.chat.mango._do_request(
                "chat/completions",
                json=payload,
                method="POST",
            )
        except TimeoutError:
            raise TimeoutMangoError()
        except ConnectionError:
            raise ConnectionMangoError()
        except Exception:
            raise ServerError()

        if stream:
            return self._stream_chunks(response, model)

        if isinstance(response, dict) and "error" in response:
            err = response["error"]
            code = err.get("code")

            if code == "model_not_found":
                raise ModelNotFoundError(model)
            elif code == "server_busy":
                raise ServerBusyError()
            elif code == "internal_error":             
                raise ServerError()
            elif err.get("type") == "rate_limit_error":
                raise RateLimitError(err.get("message"))
            elif err.get("type") == "authentication_error":
                raise AuthenticationError(err.get("message"))
            else:
                raise ResponseMangoError(status_code=500, message=err.get("message"))

        return Choices(response)

    def _stream_chunks(self, raw_stream, model):
        """
        Internal: Parses and yields streamed completion chunks.

        Args:
            raw_stream: The response stream (e.g., requests.Response with iter_lines()), or a string.
            model (str): The model name used.

        Yields:
            StreamingChoices: One chunk at a time.
        """
        
        if isinstance(raw_stream, str):
            raw_stream = io.StringIO(raw_stream)

            def iter_lines():
                for line in raw_stream:
                    yield line.encode("utf-8")
            raw_stream.iter_lines = iter_lines

            for line in raw_stream.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    data = decoded.removeprefix("data: ").strip()
                    if data == "[DONE]":
                        break
                    try:
                        parsed = json.loads(data)
                        yield StreamingChoices(parsed)
                    except json.JSONDecodeError:
                        continue
        

class Choices:
    """
    Represents a full chat completion response (non-streamed).
    """

    def __init__(self, response, **kwargs):
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


class Messages:
    """
    Represents a single message in the chat response.
    """

    def __init__(self, json, **kwargs):
        self.message = Response(json["message"])

    def __repr__(self):
        return str(self.__dict__)


class Response:
    """
    Represents the actual message content.

    Args:
        chat (dict): A dict with "role" and "content".
    """

    def __init__(self, chat, **kwargs):
        self.role = chat.get("role")
        self.content = chat.get("content")
        self.tool_calls = [ToolCall(tc) for tc in chat.get("tool_calls", [])]

    def __repr__(self):
        return str(self.__dict__)


class Usages:
    """
    Tracks token usage.

    Args:
        usage (dict): A dict with usage stats.
    """

    def __init__(self, usage):
        self.completion_tokens = usage.get("completion_tokens")
        self.prompt_tokens = usage.get("prompt_tokens")

    def __repr__(self):
        return str(self.__dict__)


class StreamingChoices:
    """
    Represents a streamed chat chunk.
    """

    def __init__(self, json):
        self.id = json.get("id")
        self.object = json.get("object")
        self.created = json.get("created")
        self.model = json.get("model")
        self.choices = [StreamingMessages(msg) for msg in json.get("choices", [])]

    def __repr__(self):
        return str(self.__dict__)


class StreamingMessages:
    """
    Represents a streamed delta message.
    """

    def __init__(self, msg):
        self.delta = StreamingResponse(msg.get("delta", {}))
        self.index = msg.get("index")
        self.finish_reason = msg.get("finish_reason")

    def __repr__(self):
        return str(self.__dict__)


class StreamingResponse:
    """
    Represents the delta in streamed response.

    Args:
        data (dict): Delta content.
    """

    def __init__(self, data):
        self.role = data.get("role")
        self.content = data.get("content")

    def __repr__(self):
        return str(self.__dict__)
        

class ToolFunction:
    """
    Represents a tool function inside a tool call.
    """

    def __init__(self, data):
        self.name = data.get("name")
        self.arguments = data.get("arguments")

    def __repr__(self):
        return str(self.__dict__)


class ToolCall:
    """
    Represents a single tool call in the message.
    """

    def __init__(self, data):
        self.id = data.get("id")
        self.index = data.get("index")
        self.finish_reason = data.get("finish_reason")
        self.type = data.get("type")
        self.function = ToolFunction(data.get("function", {}))

    def __repr__(self):
        return str(self.__dict__)
