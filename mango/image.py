import json

from .errors import ModelRequiredError, PromptRequiredError    



class Images:
    """
    Images is the main entry for image generation.

    Args:
        mango (object): The Mango API client instance.
    """

    def __init__(self, mango, **kwargs):
        self.mango = mango
        self.generations = Generations(self)


class Generations:
    """
    Provides access to image generation endpoints.

    Args:
        images (Images): Parent Images instance.
    """

    def __init__(self, images, **kwargs):
        self.images = images

    def generate(self, model: str = None, prompt: str = None, n: int = 1, size: str = "1024x1024", **kwargs):
        """
        Generates image(s) from a prompt.

        Args:
            model (str): The model ID to use (e.g., "dall-e-3").
            prompt (str): The image prompt.
            n (int): Number of images to generate.
            size (str): Image resolution like "1024x1024".            
            **kwargs: Extra arguments.

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
            "size": size,
            "quality": quality,          
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

class ImageResponse:
    """
    Represents the result of an image generation request.
    """

    def __init__(self, response):
        self.created = response.get("created")
        self.data = [Image(url=img.get("url")) for img in response.get("data", [])]

    def __repr__(self):
        return str([image.url for image in self.data])


class Image:
    """
    Represents a single generated image.

    Args:
        url (str): The image URL.
    """

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return self.url
    
