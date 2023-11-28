from PyQt6 import QtWidgets

from peracotta.peralog import logger

critical_errors = []  # error classes that should crash the program


@logger.catch()
def gui_excepthook(exc_type, exc_value, exc_tb):
    """Custom exception handler for peracotta's GUI version

    Args:
        exc_type: exception type
        exc_value: exception value
        exc_tb: exception traceback
    """
    QtWidgets.QMessageBox.warning(None, "Error", f"Peracotta encountered an exception ({exc_type.__name__}).\nSee logs for the traceback.")

    if any([exc_type is exc_t for exc_t in critical_errors]):
        QtWidgets.QApplication.quit()

    # These two lines are for pretty printing traceback with color
    # and additional info.
    # This is loguru syntax and should be modified if the logging system is changed
    options = ((exc_type, exc_value, exc_tb),) + logger._options[1:]
    logger._log("ERROR", False, options, "", None, None)
