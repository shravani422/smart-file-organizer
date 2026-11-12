import os
import time
import shutil
from categories import FILE_CATEGORIES
from history_manager import save_history
from history_manager import load_history
from utils import get_unique_filename, get_file_date
from activity_logger import log_activity


def organize_files(source_folder, organize_by_date, auto_create_folders=False):

    # Check folder exists
    if not os.path.exists(source_folder):
        print("Folder does not exist.")
        return

    folder_choices = {}
    move_history = []
    files_organized = 0
    folders_created = 0
    files_skipped = 0
    duplicates_fixed = 0

    for file_name in os.listdir(source_folder):

        file_path = os.path.join(source_folder, file_name)

        if os.path.isdir(file_path):
            continue

        file_extension = os.path.splitext(file_name)[1].lower()
        moved = False

        for category, extensions in FILE_CATEGORIES.items():

            if file_extension in extensions:

                base_category_folder = os.path.join(
                    source_folder,
                    category
                )

                if organize_by_date:

                    year, month = get_file_date(file_path)

                    category_folder = os.path.join(
                        base_category_folder,
                        year,
                        month
                    )
                else:
                    category_folder = base_category_folder

                # Folder check
                if not os.path.exists(base_category_folder):

                    if auto_create_folders:
                        folder_choices[category] = "y"

                    elif category not in folder_choices:

                        choice = input(
                            f"{category} folder does not exist. Create it? (y/n): "
                        ).lower()

                        folder_choices[category] = choice

                    if folder_choices[category] == "y":

                        os.makedirs(base_category_folder, exist_ok=True)

                        folders_created += 1
                        log_activity(f"Created folder: {base_category_folder}")

                        print(f"{category} folder created.")

                    else:
                        files_skipped += 1
                        print(f"Skipped: {file_name}")
                        moved = True
                        break

                os.makedirs(category_folder, exist_ok=True)

                destination = os.path.join(category_folder, file_name)
                original_destination = destination

                destination = get_unique_filename(destination)

                if destination != original_destination:
                    duplicates_fixed += 1
                    log_activity(f"Duplicate resolved for {file_name}")

                shutil.move(file_path, destination)

                files_organized += 1

                move_history.append({
                    "source": file_path,
                    "destination": destination
                })

                log_activity(f"Moved {file_name} → {category}")

                print(f"Moved: {file_name} → {category}")

                moved = True
                break

        # Uncategorized files
        if not moved:

            other_folder = os.path.join(source_folder, "Others")
            os.makedirs(other_folder, exist_ok=True)

            destination = os.path.join(other_folder, file_name)
            original_destination = destination

            destination = get_unique_filename(destination)

            if destination != original_destination:
                duplicates_fixed += 1
                log_activity(f"Duplicate resolved for {file_name}")

            shutil.move(file_path, destination)

            files_organized += 1

            move_history.append({
                "source": file_path,
                "destination": destination
            })

            log_activity(f"Moved {file_name} → Others")

            print(f"Moved: {file_name} → Others")

    save_history(move_history)

    print("\n===== ORGANIZATION SUMMARY =====")
    print(f"Files Organized : {files_organized}")
    print(f"Folders Created : {folders_created}")
    print(f"Files Skipped   : {files_skipped}")
    print(f"Duplicates Fixed: {duplicates_fixed}")
    print("==============================\n")
    return {
        "organized": files_organized,
        "folders": folders_created,
        "skipped": files_skipped,
        "duplicates": duplicates_fixed
    }


def undo_last_operation():

    history = load_history()

    if not history:
        print("No history found.")
        return

    for item in reversed(history):

        source = item["source"]
        destination = item["destination"]

        if os.path.exists(destination):

            shutil.move(destination, source)
            log_activity(f"Restored {os.path.basename(source)}")

            print(f"Restored: {os.path.basename(source)}")

    print("Undo completed.")


def undo_specific_file():

    history = load_history()

    if not history:
        print("No history found.")
        return

    print("\nMoved Files:")

    for index, item in enumerate(history, start=1):

        file_name = os.path.basename(item["source"])
        print(f"{index}. {file_name}")

    try:

        choice = int(input("\nEnter file number to restore: "))

        if choice < 1 or choice > len(history):
            print("Invalid choice.")
            return

        selected = history[choice - 1]

        source = selected["source"]
        destination = selected["destination"]

        if os.path.exists(destination):

            shutil.move(destination, source)
            log_activity(f"Restored specific file {os.path.basename(source)}")

            print(f"Restored: {os.path.basename(source)}")

        else:
            print("File not found.")

    except ValueError:
        print("Please enter a valid number.")


def remove_empty_folders(folder_path):

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    removed_count = 0

    for root, dirs, files in os.walk(folder_path, topdown=False):

        try:

            if not os.listdir(root):

                os.rmdir(root)
                removed_count += 1
                log_activity(f"Removed empty folder: {root}")

                print(f"Removed: {root}")

        except OSError:
            pass

    print(f"\nEmpty folders removed: {removed_count}")


def monitor_folder(folder_path, organize_by_date, duration_minutes):

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    print(f"\nWatching: {folder_path}")
    print(f"Monitoring for {duration_minutes} minute(s)...\n")

    log_activity(f"Monitoring started for {duration_minutes} minutes: {folder_path}")

    known_files = set(os.listdir(folder_path))

    start_time = time.time()
    duration_seconds = duration_minutes * 60

    while time.time() - start_time < duration_seconds:

        current_files = set(os.listdir(folder_path))
        new_files = current_files - known_files

        if new_files:

            print(f"\nDetected {len(new_files)} new file(s).")

            organize_files(
                folder_path,
                organize_by_date,
                auto_create_folders=True
            )

            known_files = set(os.listdir(folder_path))

        time.sleep(5)

    log_activity("Monitoring completed")

    print("\nMonitoring completed.")
    print("Returning to main menu...")

def organize_files_gui(source_folder, organize_by_date, auto_create_folders=False):

    return organize_files(
        source_folder,
        organize_by_date,
        auto_create_folders
    )
def get_moved_files():

    history = load_history()

    files = []

    for item in history:

        files.append(
            os.path.basename(item["source"])
        )

    return files
def undo_specific_by_index(index):

    history = load_history()

    if index < 0 or index >= len(history):
        return False

    selected = history[index]

    source = selected["source"]
    destination = selected["destination"]

    if os.path.exists(destination):

        shutil.move(destination, source)

        log_activity(
            f"Restored specific file {os.path.basename(source)}"
        )

        return True

    return False