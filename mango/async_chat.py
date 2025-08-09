import json
import io
from typing import AsyncGenerator
from .errors import ModelRequiredError, MessagesRequiredError
from .types import Choices, StreamingChoices, Messages, Response, Usages, StreamingMessages, StreamingResponse, ToolCall, ToolFunction

class AsyncChat:
    """
    Asynchronous chat functionality for the Mango API client.
    """

    def __init__(self, mango):
        self.mango = mango
        self.completions = AsyncCompletions(self)

class AsyncCompletions:
    """
    Provides access to asynchronous chat completion endpoints.

    Args:
        chat (AsyncChat): Parent AsyncChat instance.
    """

    def __init__(self, chat):
        self.chat = chat

    async def create(self, messages: list, model: str, temperature: float = None, max_completion_tokens: int = None, top_p: float = None, stop: str | list[str] | None = None, stream: bool = False, tools: list = None) -> Choices | AsyncGenerator[StreamingChoices, None]:
        """
        Creates an asynchronous chat completion.

        Args:
            messages (list): A list of message objects (dicts with role and content).
            model (str): The model ID to use.
            temperature (float, optional): Controls randomness (0.0 to 2.0). Defaults to None.
            max_completion_tokens (int, optional): Maximum tokens to generate. Defaults to None.
            top_p (float, optional): Nucleus sampling parameter. Defaults to None.
            stop (str | list[str] | None, optional): Stop sequence(s). Defaults to None.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            tools (list, optional): Tool definitions.

        Raises:
            ModelRequiredError: If model is not provided.
            MessagesRequiredError: If messages are not provided.

        Returns:
            Choices | AsyncGenerator: Parsed response or streaming chunks.
        """
        if not model:
            raise ModelRequiredError()
        if not messages:
            raise MessagesRequiredError()

        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if max_completion_tokens is not None:
            payload["max_completion_tokens"] = max_completion_tokens
        if top_p is not None:
            payload["top_p"] = top_p
        if stop is not None:
            payload["stop"] = stop
        if tools is not None:
            payload["tools"] = tools

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.chat.mango.api_key}"
        }

        response = await self.chat.mango._do_request(
            "chat/completions",
            json=payload,
            method="POST",
            headers=headers
        )

        if stream:
            return self._stream_chunks(response, model)

        return Choices(response)

    async def _stream_chunks(self, raw_stream, model) -> AsyncGenerator[StreamingChoices, None]:
        """
        Internal: Parses and yields streamed completion chunks asynchronously.

        Args:
            raw_stream: The response stream (e.g., string for streaming).
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
