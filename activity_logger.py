import os
from datetime import datetime

LOG_FILE = "activity_log.txt"


def log_activity(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def view_logs():

    if not os.path.exists(LOG_FILE):
        print("No activity log found.")
        return

    print("\n===== ACTIVITY LOG =====\n")

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.read()

        if not logs.strip():
            print("Log is empty.")
        else:
            print(logs)

    print("========================\n")
def get_logs():

    if not os.path.exists(LOG_FILE):
        return "No logs found."

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()