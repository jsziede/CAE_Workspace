"""
Reusable settings for project.
May be imported by multiple files.
"""

# System Imports.
import os, sys


# Get base directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def debug_print(*args, **kwargs):
    """
    Method to print debug statements if using runserver command.
    :param args:
    :param kwargs:
    :return:
    """
    runserver_true = len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'test', 'migrate', 'makemigrations']

    if runserver_true:
        print(*args, **kwargs)


"""
    Dev Mode and Debug.
        DEV_MODE is true if a file named "DEBUG" exists in the base project directory.
        This is done to easily separate production mode and development mode.
        Site will default to production unless debug file is explicitly created.
"""
DEBUG_FILE = os.path.join(BASE_DIR, 'DEBUG')
DEV_MODE = os.path.exists(DEBUG_FILE)
DEBUG = DEV_MODE
# debug_print("DEBUG = " + str(DEBUG))
