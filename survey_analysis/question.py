"""
This module contains classes to represent survey questions.

AbstractQuestion models the baseline for all questions which specialize into
* QuestionCollection for questions that contain subordinate questions
* Question for actual questions with associated answers by participants

.. currentmodule:: survey_analysis.question
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
from abc import ABC
from collections import defaultdict
from typing import Dict, List, Optional

from .answer import Answer


class AbstractQuestion(ABC):
    """
    AbstractQuestion provides the base for Question and QuestionCollection.

    It establishes common properties.
    Each kind of question at least has an ID and a question text accompanying
    it as provided by the survey and stored in the metadata.
    """

    def __init__(self, question_id: str, question_text: str):
        """
        Initialize a new abstract question by storing the common metadata.

        Args:
            question_id:    The ID assigned to the question by the survey
            question_text: The question text as shown to the user in the survey
        """
        self._id = question_id
        self._text = question_text

    @property
    def id(self) -> str:
        """Get the questions ID under which it was stored in the survey."""
        return self._id

    @property
    def text(self):
        """Get the question text displayed in the survey."""
        return self._text

    @property
    def has_subquestions(self) -> bool:
        """
        Check if there are sub-question associated with this question.

        Answers can only be provided to questions that have no sub-questions.

        Returns:
            False by default, True in the case of nested questions that do have
            sub-questions.
        """
        return False


class Question(AbstractQuestion):
    """
    Questions model concrete questions that could be answered in the survey.

    These questions have a set of pre-defined answers the user could choose
    from.
    Open questions that require to be answered in free text are possible by
    modelling a predefined answer that has no text set.
    Questions further contain the answers given by the participants
    respectively and provide functionality to filter these for common criteria.
    """

    def __init__(self, question_id: str,
                 question_text: str,
                 predefined_answers: List[Answer]):
        """
        Initialize a new Question with the given metadata.

        Args:
            question_id:        A unique string representing the question
            question_text:      The text of the question in the form
            predefined_answers: The answer options provided by the form
        """
        super().__init__(question_id, question_text)
        self._predefined_answers = predefined_answers
        self._given_answers: Dict[str, List[Answer]] = {}

    def __str__(self) -> str:
        """Generate a string representation of the question."""
        return f"{self.id}: {self.text} " \
               f"({len(self._predefined_answers)} predefined answers)"

    @property
    def predefined_answers(self) -> List[Answer]:
        """
        Get all pre-defined answers that were available in the form.

        In the case of boolean question there is usually one answer and it
        either shows up in the given answers or not.

        Returns:
            A list of answers that were pre-defined and could be chosen.
        """
        return self._predefined_answers

    @property
    def given_answers(self) -> Dict[str, List[Answer]]:
        """
        Get all answers that were entered by the users.

        This includes answers to free-text fields. Those answers are (usually)
        not in the list of pre-defined answers, but could be entered by the
        user.
        In the case of multiple-choice question all pre-defined answers that
        were selected by the user are contained here.

        Returns:
            A association of participants by ID with their given answers.
        """
        return self._given_answers

    def add_given_answer(self, participant_id: str, answer_text: str) -> None:
        """
        Insert an answer given by an participant for the question.

        This function is used when reading in the survey data. Make sure to
        only register answers that contain actual data via this function.

        Args:
            participant_id: The identifier for the participant that is being
                            processed
            answer_text:    The text associated with the answer as given by the
                            participant
        """
        if participant_id not in self._given_answers:
            self._given_answers[participant_id] = []

        candidates: List[Answer] = [
            answer for answer in self.predefined_answers
            if answer.text == answer_text
            ]

        new_answer: Answer = \
            candidates[0] if candidates else Answer("Free Text", answer_text)

        self._given_answers[participant_id].append(new_answer)

    def filter_given_answers(self,
                             include_predefined: bool = True,
                             include_free_text: bool = True,
                             participant_id: Optional[List[str]] = None,
                             contains_text: Optional[str] = None) \
            -> Dict[str, List[Answer]]:
        """
        Filter the answers given by participants for different conditions.

        Make sure that at least either include_predefined or include_free_text
        are set or the result will be empty.

        Args:
            include_predefined: Select answers that were predefined by
                                the question form (i.e. not free-text answers)
            include_free_text: Select answers that were not pre-defined by
                                the question form
            participant_id:     Select answers for the given participant IDs.
                                If this is None (default), all participants are
                                selected
            contains_text:      Specifies a text that must be included in the
                                answer text. The comparison is case-insensitive
                                If this is None (default) no check will be
                                performed regarding the content

        Returns:
            An association of participant IDs to the filtered answers from
            these participants. Only participants for which answers were found
            after filtering are included in the results.
        """
        assert include_free_text or include_predefined
        # TODO throw a proper exception instead
        # If neither was chosen, the result of the function will be empty...duh

        participants: List[str] = list(participant_id) if participant_id \
            else list(self._given_answers.keys())

        results: Dict[str, List[Answer]] = {}

        for participant in participants:
            answers = self._given_answers[participant]
            selected_answers = []
            for answer in answers:

                # The filters work by aborting the current iteration
                # if a condition fails, preventing them from being included
                # in the selected answers

                # Filter for the predefined/ free text property
                was_predefined: bool = answer in self._predefined_answers

                if not (
                        (include_predefined and was_predefined) or
                        (include_free_text and not was_predefined)
                ):
                    logging.debug(f"Filter: Excluding {answer} "
                                  f"(Pre-defined/Free Text Rules)")
                    continue  # will not be selected, skip to next answer

                # Filter for content
                if contains_text:
                    required_text: str = contains_text.lower()
                    searched_text: str = answer.text.lower()
                    if required_text not in searched_text:
                        logging.debug(f"Filter: Excluding {answer} "
                                      f"(Content Rules)")
                        continue  # will not be selected, skip to next answer
                selected_answers.append(answer)
            if selected_answers:
                results[participant] = selected_answers

        return results

    def grouped_by_answer(self) -> Dict[Answer, List[str]]:
        """
        Group the given answers of a question.

        Returns:
            An association between the possible answers and a list of the
            participant IDs who selected that answer.
        """
        results: Dict[Answer, List[str]] = defaultdict(list)
        for participant_id, answer_list in self.given_answers.items():
            for answer in answer_list:
                if answer.text != 'nan':
                    results[answer].append(participant_id)
        return results


class QuestionCollection(AbstractQuestion):
    """
    QuestionCollections model questions that split up into subquestions.

    This kind of question has no answers by itself. These are to be found in
    the according subquestions.
    """

    def __init__(self,
                 question_id: str,
                 question_text: str,
                 subquestions: List[Question]):
        """
        Initialize a question that contains sub-questions.

        Args:
            question_id:        A unique string representing the question
            question_text:      The text of the question in the form
            subquestions:       A list of concrete questions nested under this
                                object
        """
        super().__init__(question_id, question_text)
        self._subquestions: List[Question] = subquestions

    def __str__(self) -> str:
        """Generate a string representation of the question collection."""
        included_questions_text: str = ""

        for included_question in self._subquestions:
            included_questions_text += f"\n\t{included_question}"

        return f"{self.id}: {self.text} " \
               f"({len(self._subquestions)} nested questions)" + \
               included_questions_text

    @property
    def has_subquestions(self) -> bool:
        """
        Check if subquestions have been set for this question.

        Returns:
            True, if subquestions were provided, False otherwise.
        """
        return bool(self._subquestions)

    @property
    def subquestions(self) -> List[Question]:
        """
        Get the subquestions that were defined for this question.

        Returns:
            A list containing all the subquestions that were nested.
        """
        return self._subquestions
