import json
import os

HISTORY_FILE = "move_history.json"


def save_history(history):

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)