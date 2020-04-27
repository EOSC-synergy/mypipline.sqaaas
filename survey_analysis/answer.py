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
                 answer_text: Optional[str] = None,
                 answer_short_text: Optional[str] = None):
        """
        Initialize an Answer from the data or metadata.

        Args:
            answer_id:
                A unique string identifying the answer

            answer_text:
                If the answer is predefined, it is the text the form suggested.
                Otherwise it is the text the user entered. For pre-defining a
                free-text answer the text may be empty.

            answer_short_text:
                An optional string to be used for the string
                representation instead of the full text.
        """
        self._id: str = answer_id
        self._text: str = str(answer_text) if answer_text else ""
        self._short_text: Optional[str] = answer_short_text

    def __str__(self) -> str:
        """Generate a string representation of the answer."""
        return f"{self._id}: {self._text}"

    @property
    def id(self) -> str:
        """Obtain the ID of the answer. The ID is unique per question."""
        return self._id

    @property
    def text(self) -> str:
        """Obtain the full text that was associated with this answer."""
        return self._text

    @property
    def short_text(self) -> Optional[str]:
        """ Obtain the short text representation for the answer.

        Returns:
            The short text as string if one was set, None otherwise.
        """
        return self._short_text

    @property
    def label(self) -> str:
        """
        Obtain the shortest possible label for the answer.

            Defaults to returneing the short text.
            If no short text is defined, the full text will be used instead.

            Returns:
                the short text representation, if available,
                otherwise the full text
        """
        return self._short_text if self._short_text else self._text
