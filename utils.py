import os
from datetime import datetime

def get_unique_filename(destination):

    # If file does not exist
    if not os.path.exists(destination):
        return destination

    # Split name and extension
    filename, extension = os.path.splitext(destination)

    counter = 1

    # Keep generating new names
    while True:

        new_name = f"{filename}({counter}){extension}"

        if not os.path.exists(new_name):
            return new_name

        counter += 1

def get_file_date(file_path):

    timestamp = os.path.getmtime(file_path)

    date = datetime.fromtimestamp(timestamp)

    year = str(date.year)
    month = date.strftime("%B")

    return year, month