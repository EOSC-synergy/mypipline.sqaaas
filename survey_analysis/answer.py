"""
This module contains a class to represent survey answers.

.. currentmodule:: survey_analysis.answer
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import Optional


class Answer(object):
    """
    The Answer-class models responses to survey question.

    The use-case is twofold:
    * Answers may be used to represent pre-defined answers which could be
      selected by users
    * Answers also represent - when associated with a participant - the actual
      selection a user made.
    """

    def __init__(self,
                 answer_id: str,
                 answer_text: Optional[str] = None):
        """
        Initialize an Answer from the data or metadata.

        Args:
            answer_id:  A unique string identifying the answer
            answer_text:    If the answer is predefined, it is the text the
                            form suggested. Otherwise it is the text the user
                            entered. For pre-defining a free-text answer the
                            text may be empty.
        """
        self._id = answer_id
        self._text = answer_text if answer_text else ""

    def __str__(self) -> str:
        """Generate a string representation of the answer."""
        return f"{self._id}: {self._text}"

    @property
    def id(self) -> str:
        """Obtain the ID of the answer. The ID is unique per question."""
        return self._id

    @property
    def text(self) -> str:
        """Obtain the text that was associated with this answer."""
        return self._text
