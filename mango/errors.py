class MangoError(Exception):
    """
    Base exception for all Mango API errors.
    """
    pass


class APIKeyMissingError(MangoError):
    """
    Raised when the API key is not provided.
    """
    def __init__(self, message="API key is required."):
        super().__init__(message)


class AuthenticationError(MangoError,):
    def __init__(self, message: str = "unknown"):
        super().__init__(message)


class WordMissingError(MangoError):
    """
    Raised when no word is provided to the words() method. 
    """
    def __init__(self, message="No word provided."):
        super().__init__(message)


class ConnectionMangoError(MangoError):
    """
    Raised when there is a connection problem to the Mango API.
    """
    def __init__(self, message="Failed to connect to Mango API."):
        super().__init__(message)


class TimeoutMangoError(MangoError):
    """
    Raised when the request to the Mango API times out.
    """
    def __init__(self, message="Request to Mango API timed out."):
        super().__init__(message)


class ResponseMangoError(MangoError):
    """
    Raised when the Mango API returns an unexpected or error response.
    """
    def __init__(self, status_code: int, message: str = None):
        full_message = (
            message or f"Unexpected response from Mango API. Status code: {status_code}"
        )
        super().__init__(full_message)
        self.status_code = status_code


class ModelRequiredError(MangoError):
    """
    Raised when model is not provided in request.
    """
    def __init__(self, message="The 'model' field is required."):
        super().__init__(message)


class MessagesRequiredError(MangoError):
    """
    Raised when messages are missing in request.
    """
    def __init__(self, message="The 'messages' field is required."):
        super().__init__(message)

class PromptRequiredError(MangoError):
    """
    Raised when prompt are missing in request.
    """
    def __init__(self, message="The 'prompt' field is required."):
        super().__init__(message)
        

class ModelNotFoundError(MangoError):
    """
    Raised when the specified model does not exist.
    """
    def __init__(self, model: str = "unknown"):
        message = f"Model '{model}' not found."
        super().__init__(message)


class RateLimitError(MangoError):    
    def __init__(self, err: str = "unknown"):        
        super().__init__(err)


class ServerBusyError(MangoError):
    """
    Raised when the Mango API server is overloaded.
    """
    def __init__(self, message="Server is busy. Please try again later."):
        super().__init__(message)


class ServerError(MangoError):
    """
    Raised for unknown internal server errors.
    """
    def __init__(self, message="Unknown internal server error"):
        super().__init__(message)
