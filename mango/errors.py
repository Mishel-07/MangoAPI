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
