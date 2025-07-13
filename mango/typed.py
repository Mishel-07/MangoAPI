from typing import Any, Dict


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
