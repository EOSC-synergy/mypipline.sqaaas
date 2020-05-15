"""
This module allows discovery and dispatch of analysis functions.

.. currentmodule:: survey_analysis.dispatch
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import importlib
import logging
import traceback
from pathlib import Path
from typing import List


class Dispatcher(object):
    """
    Provides analysis function module and execution facilities.

    The operations are based on a module folder and optionally a list of
    module names to be given at initialization.
    """

    def __init__(self, module_folder: Path, module_names: List[str]):
        """
        Initialize the Dispatcher.

        Args:
            module_folder: The path to a directory containing loadable modules.
                If the given path does not exist or is not a directory a
                ValueError will be thrown.
            module_names: A list of module names (without file ending)
                within module folder to be executed.
                If the selected module does not exist in the module directory
                a ValueError will be thrown.
        """
        if not (module_folder.exists() and module_folder.is_dir()):
            raise ValueError("Module folder should be a directory.")

        self.module_folder: Path = module_folder
        self.module_names: List[str] = module_names
        self.module_name_paths: List[Path] = []
        self._discovered_modules: List[str] = []

        # Check that all selected modules exist in module folder.
        if self.module_names:
            for module_name in self.module_names:
                module_path: Path = Path(module_folder, f"{module_name}.py")
                if not module_path.exists():
                    raise ValueError(f"Module {module_name} not found in "
                                     f"module folder.")
                self.module_name_paths.append(module_path)
        else:
            self.module_name_paths.extend(self.module_folder.iterdir())

    def discover(self) -> None:
        """
        Discover all potential or selected modules in the module folder.

        Iterate over all modules in the module folder (non-recursive) or
        selected modules only and cache the names of those python (.py) files.
        Exception: __init__.py is excluded.
        """
        # Execute all scripts in scripts folder or selected scripts only.
        for name_path in self.module_name_paths:
            if (name_path.is_file()
                    and name_path.suffix == ".py"
                    and not name_path.stem == "__init__"):

                logging.info(f"Discovered module {name_path.stem}.")
                self._discovered_modules.append(name_path.stem)

    def load_all_modules(self) -> None:
        """
        Try to load and run all discovered modules.

        Make sure to run discover() beforehand.
        If no modules have been discovered, a warning will be logged.
        See Also: load_module()

        """
        if not self._discovered_modules:
            logging.warning("No modules have been discovered - Nothing to do.")
            return

        for module_name in self._discovered_modules:
            self.load_module(module_name)

    def load_module(self, module_name: str) -> None:
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
        logging.info(f"Running Module {module_dot_path}.")

        try:
            module = importlib.import_module(module_dot_path)
        except ImportError:
            logging.error(f"Failed to load module {module_dot_path}.")

        try:
            module.run()
        except AttributeError as error:
            traceback.print_exc()
            logging.error(f"Module {module_dot_path}: "
                          f"Error when calling run() - method: "
                          f"{error}.")
