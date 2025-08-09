from .errors import ModelRequiredError, PromptRequiredError
from .types import ImageResponse, Image

class AsyncImages:
    """
    Asynchronous image functionality for the Mango API client.
    """

    def __init__(self, mango):
        self.mango = mango
        self.generations = AsyncGenerations(self)

class AsyncGenerations:
    """
    Provides access to asynchronous image generation endpoints.

    Args:
        images (AsyncImages): Parent AsyncImages instance.
    """

    def __init__(self, images):
        self.images = images

    async def generate(self, model: str, prompt: str, n: int = 1, size: str = "1024x1024") -> ImageResponse:
        """
        Asynchronously generates image(s) from a prompt.

        Args:
            model (str): The model ID to use (e.g., "mango-image-model").
            prompt (str): The image prompt.
            n (int, optional): Number of images to generate. Defaults to 1.
            size (str, optional): Image resolution like "1024x1024". Defaults to "1024x1024".

        Returns:
            ImageResponse: Parsed image generation result.
        """
        if not model:
            raise ModelRequiredError()
        if not prompt:
            raise PromptRequiredError()

        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.images.mango.api_key}"
        }

        response = await self.images.mango._do_request(
            "images/generations",
            json=payload,
            method="POST",
            headers=headers
        )

        return ImageResponse(response)
