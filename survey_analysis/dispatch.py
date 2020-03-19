"""
This module allows discovery and dispatch of analysis functions.

.. currentmodule:: survey_analysis.dispatch
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import importlib
import logging
from pathlib import Path
from typing import List


class Dispatcher(object):
    """
    Provides analysis function module and execution facilities.

    The operations are based on a module folder to be given at initialization.
    """

    def __init__(self, module_folder: Path):
        """
        Initialize the Dispatcher.

        Args:
            module_folder: The path to a directory containing loadable modules.
            If the given path does not exist or is not a directory a ValueError
            will be thrown.
        """
        if not (module_folder.exists() and module_folder.is_dir()):
            raise ValueError("Module folder should be a directory")

        self.module_folder: Path = module_folder
        self._discovered_modules: List[str] = list()

    def discover(self) -> None:
        """
        Discover all potential modules in the module folder.

        Iterate over the module folder (non-recursive) and cache the names all
        python (.py) files.
        Exception: __init__.py is excluded.
        """
        for entry in self.module_folder.iterdir():
            if entry.is_file() \
                    and entry.suffix == ".py" \
                    and not entry.stem == "__init__":
                logging.info(f"Discovered module {entry.stem}")
                self._discovered_modules.append(entry.stem)

    def load_all_modules(self):
        """
        Try to load and run all discovered modules.

        Make sure to run discover() beforehand.
        If no modules have been discovered, a warning will be logged.
        See Also: load_module()

        """
        if not self._discovered_modules:
            logging.warning("No modules have been discovered - Nothing to do")
            return

        for module_name in self._discovered_modules:
            self.load_module(module_name)

    def load_module(self, module_name: str):
        """
        Attempt to load a module given by name.

        Exceptions raised from import will be caught and logged as error on
        the console.

        Args:
            module_name: The name of the module, without the .py ending

        """
        # TODO if the module_name has a .py ending, remove it beforehand

        module_path: Path = self.module_folder / module_name
        module_dot_path: str = str(module_path).replace('/', '.')
        logging.info(f"Running Module {module_dot_path}")

        try:
            module = importlib.import_module(module_dot_path)
            module.run()
        except ImportError:
            logging.error(f"Failed to load module {module_dot_path}")
        except AttributeError:
            logging.error(f"Module {module_dot_path} has no run() - method")
