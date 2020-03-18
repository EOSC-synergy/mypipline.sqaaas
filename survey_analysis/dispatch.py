"""
This module contains facilities for dynamic discovery and dispatch of analysis
functions.

.. currentmodule:: survey_analysis.dispatch
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import importlib
import logging
from pathlib import Path


class Dispatcher(object):

    def __init__(self, module_folder: Path):
        self.module_folder: Path = module_folder

    def load_module(self, module_name: str):
        # TODO if the module_name has a .py ending, remove it beforehand

        module_path: Path = self.module_folder / module_name
        module_dot_path: str = str(module_path).replace('/', '.')
        logging.info(f"Processing Module {module_dot_path}")

        try:
            module = importlib.import_module(module_dot_path)
            module.run()
        except ImportError:
            logging.error(f"Failed to load module {module_dot_path}")
        except AttributeError:
            logging.error(f"Module {module_dot_path} has no run() - method")
