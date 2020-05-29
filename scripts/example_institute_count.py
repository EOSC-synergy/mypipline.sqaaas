"""
A dummy script for testing the function dispatch

.. currentmodule:: survey_analysis.scripts.example_institute_count.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import Dict, List

from survey_analysis import globals
from survey_analysis.answer import Answer
from survey_analysis.question import Question


def run():
    print("Example Script: Counting Answers for Question G1003")

    # As an example, count how many participants there were for each
    # institution

    question: Question = globals.survey_questions["G1003"]

    print(f"\t{question.text}")

    valid_answers: Dict[str, List[Answer]] = \
        question.filter_given_answers(include_free_text=False)

    counted_answers: Dict[Answer, int] = {}

    # valid_answers yields the participant ID as well which we do not need for
    # this use case. That is why the .values() is used here

    # Flatten the obtained list of lists
    # See also https://stackoverflow.com/questions/952914/how-to-make-a-flat
    # -list-out-of-list-of-lists
    answers: List[Answer] = [
        item
        for sublist in valid_answers.values()
        for item in sublist
        ]

    answer: Answer
    for answer in answers:
        if answer in counted_answers:
            counted_answers[answer] += 1
        else:
            counted_answers[answer] = 1

    for answer in counted_answers:
        print(f"{counted_answers[answer]:>4} \t{answer.text}")
