"""
This module contains facilities for dynamic discovery and dispatch of analysis
functions.

.. currentmodule:: survey_analysis.dispatch
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from types import ModuleType


class Dispatcher(object):

    def __init__(self, module_folder):
        self.module_folder = module_folder

    def load_module(self, module_name: str):
        # TODO if the module_name has a -py ending, remove it beforehand

        full_path: str = self.module_folder + module_name
        full_path.replace('/', '.')
        module: ModuleType = __import__(full_path, fromlist=[''])
        # TODO check if module was loaded properly

        self.dispatch(module)

    def dispatch(self, module: ModuleType):
        # TODO check if the module has the required function
        module.run()
