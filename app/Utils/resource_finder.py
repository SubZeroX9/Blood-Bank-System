import os
import sys

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # The application is frozen/compiled
        app_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        # app_path = os.path.abspath('.')
    else:
        # The application is not frozen/compiled
        app_path = os.path.abspath('./app')

    return os.path.join(app_path, relative_path)
