import os
import sys

def bot_import():
    current_dir = os.path.dirname(__file__)
    path_bot = os.path.abspath(os.path.join(current_dir, ".."))

    sys.path.append(path_bot)

    from bot import bot