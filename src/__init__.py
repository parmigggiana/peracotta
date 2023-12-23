"""
Python package `peracotta` provides a program intended to gather hardware data, display it and upload it to [T.A.R.A.L.L.O.](https://github.com/weee-open/tarallo).

The following documentation is intended for future mantainers and developers working on peracotta, and doesn't aim to be a clean easy-to-use user guide, although it may still prove useful in that sense.

Docs are automatically generated by [`pdoc3`](https://pdoc3.github.io/) using docstrings (following [PEP 257](https://peps.python.org/pep-0257/) conventions).

## Packaging
The packaging is done using [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) and [`setuptools`](https://setuptools.pypa.io/en/latest/)

Even if you're not familiar with this setup, simply reading the `pyproject.toml` file should be pretty self-explanatory.
Some interesting properties are:

 - **[project.scripts]** define commands that will be installed in the system (usually in ~/.local/bin, make sure it's in PATH) and what functions in the package they should call.
 - **[project.gui-scripts]** same thing but for commands that start a GUI.
 - **[tool.setuptools.package-data]** by default, only .py files are included in the built package. This property allows including useful data files such as assets and scripts. Find more info [here](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#package-data).

## Styling
as a general rule for styling try to follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). Formatting is done with black and isort (installed as a pre-commit hook).

## Contributing
You should **NEVER** push directly to the master branch.
Work on each feature/improvement/bugfix in a separate branch (usually in a fork in your personal github profile).

If two or more branches need to be merged together don't merge both in master, but first merge one into the other and resolve conflicts, then merge into master.

Only ever merge into master if all tests are passing.

When merging a branch, only use the 'rebase' option if there isn't more than a couple of commits. Otherwise, prefer 'squash'.

Be coincise and descriptive with your commits.
Avoid nonsensical or ambiguous descriptions, they will only make your life miserable when a new bug is found tomorrow and you have to trace back the root cause.

If you modify existing code make sure you keep the documentation up-to-date.
Mostly, the documentation is done through docstrings so it should be easy.
The docstrings should ideally be updated in the same commit that modified the interested code.

## Adding new features
Whenever a new feature is added make sure that you have added proper tests and documentation before merging
"""

import signal
import sys

from PyQt6 import QtWidgets

from . import peracruda
from .commons import env_to_bool
from .config import CONFIG
from .constants import VERSION
from .gui import GUI, errored, gui_excepthook
from .peralog import logdir, logger
from .reporter import send_report


def parse_common_args():
    """Parse arguments common to both GUI and CLI version
    --version prints the current version and quits.
    --logs prints the path where logs are stored and quits.
    """
    if any([s in sys.argv for s in ["--version", "-v"]]):
        print(f"P.E.R.A.C.O.T.T.A. Version {VERSION}")
        exit(0)

    if "--logs" in sys.argv:
        print(f"P.E.R.A.C.O.T.T.A.'s logs are located in {logdir.as_posix()}")
        exit(0)


def main_gui():
    """Entrypoint for the GUI version."""
    parse_common_args()

    sys.excepthook = gui_excepthook
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # makes CTRL+ C work

    app = QtWidgets.QApplication(sys.argv)

    # noinspection PyUnusedLocal
    window = GUI(app)
    app.exec()

    if CONFIG["AUTOMATIC_REPORT_ERRORS"] and errored():
        try:
            send_report()
        except Exception as e:
            logger.info("Couldn't upload crash log.")
            logger.exception(e)


def main_cli():
    """.. todo::Entrypoint for the CLI version"""
    print("Sorry, peracruda isn't implemented in v2 yet! Use the old one at https://github.com/WEEE-Open/peracotta")
    parse_common_args()
    # peracruda.main_()
