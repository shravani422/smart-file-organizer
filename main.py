from organizer import (
    organize_files,
    undo_last_operation,
    undo_specific_file,
    remove_empty_folders,
    monitor_folder
)
from activity_logger import view_logs
while True:

    print("1. Organize Files")
    print("2. Undo Last Operation")
    print("3. Undo Specific File")
    print("4. Remove Empty Folders")
    print("5. Start Folder Monitoring")
    print("6. view activity log")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        folder_path = input("Enter folder path: ")

        date_choice = input(
            "Organize files by date? (y/n): "
        ).lower()

        organize_files(
            folder_path,
            date_choice == "y"
        )

    elif choice == "2":

        undo_last_operation()

    elif choice == "3":

        undo_specific_file()


    elif choice == "4":

        folder_path = input(

            "Enter folder path: "

        )

        remove_empty_folders(folder_path)

    elif choice == "5":

        folder_path = input(
            "Enter folder path: "
        )

        date_choice = input(
            "Organize files by date? (y/n): "
        ).lower()

        duration = int(
            input("Monitor for how many minutes? ")
        )

        monitor_folder(
            folder_path,
            date_choice == "y",
            duration
        )
    elif choice == "6":
        view_logs()

    elif choice=="7":
         break

    else:

        print("Invalid choice.")