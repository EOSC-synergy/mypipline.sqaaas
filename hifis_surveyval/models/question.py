# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
This module contains classes to represent survey questions.

AbstractQuestion models the baseline for all questions which specialize into
* QuestionCollection for questions that contain subordinate questions
* Question for actual questions with associated answers by participants

.. currentmodule:: hifis_surveyval.models.question
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy
from pandas import DataFrame, Series

from hifis_surveyval.models.answer import Answer, AnswerType


class AbstractQuestion(ABC):
    """
    AbstractQuestion provides the base for Question and QuestionCollection.

    It establishes common properties.
    Each kind of question at least has an ID and a question text accompanying
    it as provided by the survey and stored in the metadata.
    """

    def __init__(self, question_id: str, question_text: str) -> None:
        """
        Initialize a new abstract question by storing the common metadata.

        Args:
            question_id (str): The ID assigned to the question by the survey.
            question_text (str): The question text as shown to the user in the
                                 survey.
        """
        self._id = question_id
        self._text = question_text

    @property
    def id(self) -> str:
        """
        Get the questions ID under which it was stored in the survey.

        Returns:
            str: Question ID.
        """
        return self._id

    @property
    def text(self):
        """
        Get the question text displayed in the survey.

        Returns:
            str: Question text.
        """
        return self._text

    @property
    def has_subquestions(self) -> bool:
        """
        Check if there are sub-question associated with this question.

        Answers can only be provided to questions that have no sub-questions.

        Returns:
           bool: False by default, True in the case of nested questions that
                 do have sub-questions.
        """
        return False

    @abstractmethod
    def flatten(self) -> List["Question"]:
        """
        Provide a unified flat representation of the questions structure.

        Returns:
            List[Question]: A list either containing the question itself or
                            all concrete sub-questions.
        """
        pass


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

    def __init__(
        self,
        question_id: str,
        question_text: str,
        predefined_answers: List[Answer],
        answers_data_type: type = str,
    ) -> None:
        """
        Initialize a new Question with the given metadata.

        Args:
            question_id (str): A unique string representing the question.
            question_text (str): The text of the question in the form.
            predefined_answers (List[Answer]): The answer options provided by
                                               the form.
            answers_data_type (type): The type of answers given by participants
                                      (str [default], bool, int, float).

        Raises:
            ValueError: Exception thrown if data type is not given.
            TypeError: Exception thrown if data types do not match.
        """
        if answers_data_type is None:
            raise ValueError(
                f"Attempt to construct question {question_id} "
                f"with answer type 'None'"
            )

        super().__init__(question_id, question_text)
        # Check that type of answer data matches type of question data and
        # raise TypeError if they do not match.
        for answer in predefined_answers:
            if answer.data_type is not answers_data_type:
                raise TypeError(
                    f"Type of answer {answer.id} "
                    f"'{answer.text}' "
                    f"(type '{answer.data_type.__name__}') "
                    f"is not equal to expected type "
                    f"'{answers_data_type.__name__}'."
                )
        self._predefined_answers = predefined_answers
        self._given_answers: Dict[str, List[Answer]] = {}
        self._data_type: type = answers_data_type

    def __str__(self) -> str:
        """
        Generate a string representation of the question.

        Returns:
            str: String representation of the question.
        """
        return (
            f"{self.id}: {self.text} "
            f"({len(self._predefined_answers)} predefined answers)"
        )

    @property
    def data_type(self) -> type:
        """
        Get the type of data of a question.

        Questions have a data type which determines how to process the data
        depending on the type. Possible data types are str (default), bool,
        int, float.

        Returns:
            type: The type of data to this question.
        """
        return self._data_type

    @property
    def predefined_answers(self) -> List[Answer]:
        """
        Get all pre-defined answers that were available in the form.

        In the case of boolean question there is usually one answer and it
        either shows up in the given answers or not.

        Returns:
            List[Answer]: A list of answers that were pre-defined and could
                          be chosen.
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
            Dict[str, List[Answer]]: A association of participants by ID with
                                     their given answers.
        """
        return self._given_answers

    def add_given_answer(
        self, participant_id: str, answer_data: Optional[AnswerType]
    ) -> None:
        """
        Insert an answer given by an participant for the question.

        This function is used when reading in the survey data. Make sure to
        only register answers that contain actual data via this function.

        Args:
            participant_id (str): The identifier for the participant that is
                                  being processed.
            answer_data (Optional[AnswerType): The text associated with the
                                               answer as given by the
                                               participant. Its type should
                                               match the question data type.

        Raises:
            TypeError: Exception thrown if data types do not match.
        """
        if (
            not type(answer_data) == self._data_type
            and answer_data is not None
        ):
            raise TypeError(
                f"Answer data type did not match question type. "
                f"Answer was {answer_data} "
                f"(type '{type(answer_data).__name__}') "
                f"for participant {participant_id}, "
                f"but question {self._id} expected type "
                f"'{self._data_type.__name__}'."
            )

        if participant_id not in self._given_answers:
            self._given_answers[participant_id] = []

        candidates: List[Answer] = [
            answer
            for answer in self.predefined_answers
            if answer.raw_data == answer_data
        ]

        new_answer: Answer = (
            candidates[0]
            if candidates
            else Answer(
                answer_id="Free Text",
                answer_data=answer_data,
                answer_short_text=None,
                answer_data_type=self._data_type,
            )
        )

        self._given_answers[participant_id].append(new_answer)

    def filter_given_answers(
        self,
        include_predefined: bool = True,
        include_free_text: bool = True,
        participant_id: Optional[List[str]] = None,
        contains_text: Optional[str] = None,
    ) -> Dict[str, List[Answer]]:
        """
        Filter the answers given by participants for different conditions.

        Make sure that at least either include_predefined or include_free_text
        are set or the result will be empty.

        Args:
            include_predefined (bool): Select answers that were predefined by
                                       the question form (i.e. not free-text
                                       answers).
            include_free_text (bool): Select answers that were not pre-defined
                                      by the question form.
            participant_id (Optional[List[str]]): Select answers for the
                                                  given participant IDs.
                                                  If this is None (default),
                                                  all participants are
                                                  selected.
            contains_text (Optional[str]): Specifies a text that must be
                                           included in the answer text.
                                           The comparison is case-insensitive.
                                           If this is None (default) no check
                                           will be performed regarding the
                                           content.

        Returns:
            Dict[str, List[Answer]]: An association of participant IDs to the
                                     filtered answers from these participants.
                                     Only participants for which answers were
                                     found after filtering are included in the
                                     results.
        """
        assert include_free_text or include_predefined
        # TODO throw a proper exception instead
        # If neither was chosen, the result of the function will be empty...duh

        participants: List[str] = (
            list(participant_id)
            if participant_id
            else list(self._given_answers.keys())
        )

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
                    (include_predefined and was_predefined)
                    or (include_free_text and not was_predefined)
                ):
                    logging.debug(
                        f"Filter: Excluding {answer} "
                        f"(Pre-defined/Free Text Rules)"
                    )
                    continue  # will not be selected, skip to next answer

                # Filter for content
                if contains_text:
                    required_text: str = contains_text.lower()
                    searched_text: str = answer.text.lower()
                    if required_text not in searched_text:
                        logging.debug(
                            f"Filter: Excluding {answer} " f"(Content Rules)"
                        )
                        continue  # will not be selected, skip to next answer
                selected_answers.append(answer)
            if selected_answers:
                results[participant] = selected_answers

        return results

    def grouped_by_answer(self) -> Dict[Answer, List[str]]:
        """
        Group the given answers of a question.

        Returns:
            Dict[Answer, List[str]]: An association between the possible
                                     answers and a list of the participant IDs
                                     who selected that answer.
        """
        results: Dict[Answer, List[str]] = defaultdict(list)
        nan_answer: Answer = Answer("Free Text", "nan")
        for participant_id, answer_list in self.given_answers.items():
            for answer in answer_list:
                if answer.text == "nan":
                    results[nan_answer].append(participant_id)
                else:
                    results[answer].append(participant_id)
        return results

    def flatten(self) -> List["Question"]:
        """
        Provide a flattened list representation of the question.

        Returns:
            List[Question]: A list containing the question itself.
        """
        return [self]

    def as_series(
        self, filter_invalid: bool = True, use_short_answer: bool = False
    ) -> Series:
        """
        Create a pandas series from a given question.

        The answers given to the question by participants will be converted
        to a data type given in the metadata of the question in order to
        be able to process the given answers depending on this data type
        (e.g. removing invalid data like NaN from the pandas series).
        If for a given Question more than one answer is provided per
        participant, the data is not uni-variate and therefore the result may
        be unexpected by omitting answers from the provided data.

        Args:
            filter_invalid (bool): Whether to remove invalid data entries.
                                   Will remove data entries considered invalid
                                   by pandas if set to True, which is the
                                   default.
            use_short_answer (bool): Use the short version of the answer
                                     instead of the raw data, if available.
                                     Especially useful if the answer would
                                     generate very long labels.
                                     Default is False.

        Returns:
            Series: A new pandas series from the given answers, with
                    participant IDs as index.

        Raises:
            ValueError: Exception thrown if multi-variate data is at hand
                        which can not be converted into a Series.
        """
        question_answers: List[AnswerType] = []

        participant_id: str
        for participant_id in self.given_answers:

            assert len(self._given_answers[participant_id])
            # Should have had answer if participant id is a key

            # (0) Assume univariate data, only take first element
            # Should not have multiple elements
            if len(self._given_answers[participant_id]) > 1:  # See Note (0)
                raise ValueError(
                    "Multivariate data can not be " "converted to series"
                )

            answer = self.given_answers[participant_id][0]  # See Note (0)

            if use_short_answer and answer.short_text:
                question_answers.append(answer.short_text)
            else:
                question_answers.append(answer.raw_data)

        series = Series(
            data=question_answers,
            index=self.given_answers.keys(),
            copy=True,
            name=self.id + " Series",
        )

        if self.data_type == str:
            series.replace("nan", numpy.NaN, inplace=True)

        if filter_invalid:
            series.dropna(inplace=True)
        series = series.astype(self._data_type.__name__)
        return series

    def as_counted_series(
        self,
        relative_values: bool = False,
        filter_invalid: bool = True,
        use_short_answer: bool = False,
    ) -> Series:
        """
        Count the occurrence of given answers.

        The occurrences of given answers to a question is counted
        in a pandas series. The value counts can be calculated
        as relative values and NaN values can be removed along
        the way.

        Args:
            relative_values (bool): Instead of absolute counts fill the
                                    cells with their relative contribution
                                    to the column total. Defaults to False.
            filter_invalid (bool): Whether to remove the NaN / None value
                                   count. Defaults to True.
            use_short_answer (bool): Use the short version of the answer
                                     instead of the raw data, if available.
                                     Especially useful if the answer would
                                     generate very long labels.
                                     Default is False.

        Returns:
            Series: A series containing the count per answer.
        """
        as_series = self.as_series(
            filter_invalid=filter_invalid, use_short_answer=use_short_answer
        )

        return as_series.value_counts(
            normalize=relative_values, dropna=filter_invalid
        )


class QuestionCollection(AbstractQuestion):
    """
    QuestionCollections model questions that split up into sub-questions.

    This kind of question has no answers by itself. These are to be found in
    the according sub-questions.
    """

    def __init__(
        self,
        question_id: str,
        question_text: str,
        subquestions: List[Question],
    ) -> None:
        """
        Initialize a question that contains sub-questions.

        Args:
            question_id (str): A unique string representing the question.
            question_text (str): The text of the question in the form.
            subquestions (List[Question]): A list of concrete questions nested
                                           under this object.
        """
        super().__init__(question_id, question_text)
        self._subquestions: List[Question] = subquestions

    def __str__(self) -> str:
        """
        Generate a string representation of the question collection.

        Returns:
            str: String representation of the question collection.
        """
        included_questions_text: str = ""

        for included_question in self._subquestions:
            included_questions_text += f"\n\t{included_question}"

        return (
            f"{self.id}: {self.text} "
            f"({len(self._subquestions)} nested questions)"
            + included_questions_text
        )

    @property
    def has_subquestions(self) -> bool:
        """
        Check if sub-questions have been set for this question.

        Returns:
            bool: True, if sub-questions were provided, False otherwise.
        """
        return bool(self._subquestions)

    @property
    def subquestions(self) -> List[Question]:
        """
        Get the sub-questions that were defined for this question.

        Returns:
            List[Question]: A list containing all the sub-questions that were
                            nested.
        """
        return self._subquestions

    def flatten(self) -> List[Question]:
        """
        Provide a flattened list representation of the question collection.

        Returns:
            List[Question]: A list containing all the sub-questions.
        """
        return self._subquestions

    def collapse(self) -> Question:
        """
        Attempt to collapse the question collection into a singular question.

        This method is primarily intended to convert question collections that
        represent multiple-choice questions with boolean options into a
        singular question.

        Boolean sub-questions will be transformed to predefined answers, any
        answer to the boolean questions that resulted in True will be counted
        as a given answer on the base of the newly created predefined question.
        Non-boolean question answers will be counted as individual given
        answers and the answer text will be prefixed with the question text in
        parenthesis.

        The ID of the generated question will be the collection ID with an
        asterisk as postfix.
        The type of the generated question will be str.

        Returns:
            Question: A Question subsuming the answers given in the
                      sub-questions of the collection.
        """
        predefined_answers: List[Answer] = []
        given_answers: List[Tuple[str, str]] = []

        # Extract the new predefined answers and given answers
        subquestion: Question
        for subquestion in self._subquestions:
            if subquestion.data_type is bool:
                new_answer: Answer = Answer(
                    answer_id=subquestion.id, answer_data=subquestion.text
                )
                predefined_answers.append(new_answer)

                answers: List[Answer]
                participant: str
                for participant in subquestion.given_answers:
                    answers = subquestion.given_answers[participant]
                    assert len(answers) == 1

                    if not (answers[0].raw_data is True):
                        continue
                    given_answers.append((participant, new_answer.raw_data))
            else:
                for participant in subquestion.given_answers:
                    for answer in subquestion.given_answers[participant]:
                        given_answers.append(
                            (  # Parenthesis for tuple
                                participant,
                                f"({subquestion.text}) {answer.text}",
                            )
                        )

        # Generate the new question and fill in the given data
        new_question = Question(
            question_id=f"{self.id}*",
            question_text=self.text,
            predefined_answers=predefined_answers,
        )

        for (participant, answer) in given_answers:
            new_question.add_given_answer(participant, answer)

        return new_question

    def as_dataframe(self, question_text_as_id: bool = False) -> DataFrame:
        """
        Generate a composition of answers for the sub-questions as a dataframe.

        The data frame is constructed by obtaining each question as series and
        merging them together.
        The resulting dataframe may contain NaN-values as a result.

        Args:
            question_text_as_id (bool): Indicates whether to use the text of
                                        the sub-question as column names of
                                        the data frame, instead of the
                                        sub-question ids.
                                        Defaults to False.

        Returns:
            DataFrame: A data frame containing the answer data with
                       sub-questions as columns and participant ids as indices.
        """
        collected_data: Dict[str, Series] = {}
        for question in self._subquestions:
            series = question.as_series(filter_invalid=False)
            if question_text_as_id:
                collected_data[question.text] = series
            else:
                collected_data[question.id] = series

        return DataFrame(collected_data)
