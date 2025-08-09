from .errors import ModelRequiredError, PromptRequiredError
from .types import ImageResponse, Image

class Images:
    """
    Images is the main entry for image generation.

    Args:
        mango (object): The Mango API client instance.
    """

    def __init__(self, mango):
        self.mango = mango
        self.generations = Generations(self)

class Generations:
    """
    Provides access to image generation endpoints.

    Args:
        images (Images): Parent Images instance.
    """

    def __init__(self, images):
        self.images = images

    def generate(self, model: str, prompt: str, n: int = 1, size: str = "1024x1024"):
        """
        Generates image(s) from a prompt.

        Args:
            model (str): The model ID to use (e.g., "mango-image-model").
            prompt (str): The image prompt.
            n (int, optional): Number of images to generate. Defaults to 1.
            size (str, optional): Image resolution like "1024x1024". Defaults to "1024x1024".

        Raises:
            ModelRequiredError: If model is not provided.
            PromptRequiredError: If prompt is not provided.

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

        response = self.images.mango._do_request(
            "images/generations",
            json=payload,
            method="POST",
            headers=headers
        )

        return ImageResponse(response)
