import customtkinter as ctk
import threading
from tkinter import filedialog, messagebox

from organizer import (
    organize_files_gui,
    undo_last_operation,
    remove_empty_folders,
    monitor_folder,
    get_moved_files,
    undo_specific_by_index
)
from activity_logger import get_logs

# ---------- THEME ----------
BG = "#F8F4F2"
CARD = "#FFFFFF"
ACCENT = "#C98C8C"
ACCENT_HOVER = "#B97777"
TEXT = "#2F2F2F"
SUBTEXT = "#7A7A7A"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart File Organizer Pro")
app.geometry("1400x850")
app.configure(fg_color=BG)

folder_path = ctk.StringVar()
status_var = ctk.StringVar(value="Ready")

stats = {
    "organized": 0,
    "folders": 0,
    "skipped": 0,
    "duplicates": 0
}


def run_thread(func):
    threading.Thread(target=func, daemon=True).start()


def select_folder():
    path = filedialog.askdirectory()
    if path:
        folder_path.set(path)
        folder_label.configure(text=path)
        status_var.set(
            f"Selected: {path.split('/')[-1]}"
        )

def refresh_logs():

    logs = get_logs()

    # Right panel
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.insert("end", logs)
    log_box.configure(state="disabled")

    # Recent activity panel
    activity_box.configure(state="normal")
    activity_box.delete("1.0", "end")

    lines = logs.splitlines()

    for line in reversed(lines[-10:]):
        activity_box.insert("end", f"• {line}\n\n")

    activity_box.configure(state="disabled")

def update_cards(result):

    if not result:
        return

    stats["organized"] += result["organized"]
    stats["folders"] += result["folders"]
    stats["skipped"] += result["skipped"]
    stats["duplicates"] += result["duplicates"]

    organized_value.configure(
        text=str(stats["organized"])
    )

    folders_value.configure(
        text=str(stats["folders"])
    )

    skipped_value.configure(
        text=str(stats["skipped"])
    )

    duplicates_value.configure(
        text=str(stats["duplicates"])
    )


def organize_action():
    if not folder_path.get():
        messagebox.showwarning("Folder", "Select a folder first.")
        return

    def task():
        status_var.set("Organizing files...")

        result = organize_files_gui(
            folder_path.get(),
            True,
            True
        )

        app.after(0, lambda: update_cards(result))
        app.after(0, refresh_logs)
        app.after(0, lambda: status_var.set("Organization completed"))

    run_thread(task)


def undo_last():

    def task():

        status_var.set(
            "Restoring files..."
        )

        undo_last_operation()

        app.after(0, refresh_logs)

        app.after(
            0,
            lambda: status_var.set(
                "Undo completed"
            )
        )

    run_thread(task)


def remove_empty():
    if not folder_path.get():
        return

    def task():

        status_var.set("Removing empty folders...")

        remove_empty_folders(folder_path.get())

        app.after(0, refresh_logs)

        app.after(
            0,
            lambda: status_var.set(
                "Empty folders removed"
            )
        )

    run_thread(task)


def start_monitoring():
    if not folder_path.get():
        return

    def task():
        monitor_folder(
            folder_path.get(),
            True,
            1
        )

        app.after(0, refresh_logs)
        app.after(0, lambda: status_var.set("Monitoring completed"))

    run_thread(task)
    status_var.set(
        "Monitoring active (1 minute)"
    )

def undo_specific_popup():
    popup = ctk.CTkToplevel(app)
    popup.title("Undo Specific File")
    popup.geometry("500x500")

    files = get_moved_files()

    listbox = ctk.CTkScrollableFrame(popup)
    listbox.pack(fill="both", expand=True, padx=20, pady=20)

    selected = ctk.IntVar(value=-1)

    for i, name in enumerate(files):
        ctk.CTkRadioButton(
            listbox,
            text=name,
            variable=selected,
            value=i
        ).pack(anchor="w", pady=5)

    def restore():
        index = selected.get()

        if index >= 0:
            success = undo_specific_by_index(index)

            if success:
                refresh_logs()
                status_var.set("File restored")
                popup.destroy()
    ctk.CTkButton(
        popup,
        text="Restore Selected",
        fg_color=ACCENT,
        hover_color=ACCENT_HOVER,
        command=restore
    ).pack(pady=15)


# ---------- SIDEBAR ----------
sidebar = ctk.CTkFrame(
    app,
    width=320,
    fg_color=CARD,
    corner_radius=25
)
sidebar.pack(side="left", fill="y", padx=15, pady=15)
sidebar.pack_propagate(False)

ctk.CTkLabel(
    sidebar,
    text="SMART FILE\nORGANIZER",
    font=("Segoe UI", 28, "bold"),
    text_color=TEXT
).pack(pady=30)


def side_button(text, command):
    btn = ctk.CTkButton(
        sidebar,
        text=text,
        command=command,
        height=50,
        corner_radius=14,
        fg_color=ACCENT,
        hover_color=ACCENT_HOVER,
        font=("Segoe UI", 15, "bold")
    )
    btn.pack(fill="x", padx=20, pady=8)


side_button("Select Folder", select_folder)
side_button("Organize Files", organize_action)
side_button("Start Monitoring", start_monitoring)
side_button("Undo Last", undo_last)
side_button("Undo Specific", undo_specific_popup)
side_button("Remove Empty Folders", remove_empty)
side_button("Refresh Logs", refresh_logs)

# ---------- CENTER ----------
center = ctk.CTkFrame(app, fg_color=BG)
center.pack(side="left", fill="both", expand=True, padx=10, pady=15)

ctk.CTkLabel(
    center,
    text="Dashboard",
    font=("Segoe UI", 34, "bold"),
    text_color=TEXT
).pack(anchor="w", pady=(10, 5))

folder_label = ctk.CTkLabel(
    center,
    text="No folder selected",
    text_color=SUBTEXT,
    font=("Segoe UI", 14)
)
folder_label.pack(anchor="w")

ctk.CTkLabel(
    center,
    textvariable=status_var,
    text_color=SUBTEXT
).pack(anchor="w", pady=(0, 20))

cards_frame = ctk.CTkFrame(center, fg_color=BG)
cards_frame.pack(fill="x")


def create_card(parent, title):
    frame = ctk.CTkFrame(
        parent,
        width=180,
        height=120,
        fg_color=CARD,
        corner_radius=20
    )
    frame.pack(side="left", padx=10)

    ctk.CTkLabel(
        frame,
        text=title,
        text_color=SUBTEXT
    ).pack(pady=(20, 5))

    value = ctk.CTkLabel(
        frame,
        text="0",
        font=("Segoe UI", 28, "bold")
    )
    value.pack()

    return value


organized_value = create_card(cards_frame, "Files Organized")
folders_value = create_card(cards_frame, "Folders Created")
skipped_value = create_card(cards_frame, "Files Skipped")
duplicates_value = create_card(cards_frame, "Duplicates Fixed")

recent_frame = ctk.CTkFrame(
    center,
    fg_color=CARD,
    corner_radius=20
)
recent_frame.pack(fill="both", expand=True, pady=25)

ctk.CTkLabel(
    recent_frame,
    text="Recent Activity",
    font=("Segoe UI", 20, "bold")
).pack(anchor="w", padx=20, pady=15)

activity_box = ctk.CTkTextbox(recent_frame)
activity_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# ---------- RIGHT ----------
right = ctk.CTkFrame(
    app,
    width=350,
    fg_color=CARD,
    corner_radius=25
)
right.pack(side="right", fill="y", padx=15, pady=15)
right.pack_propagate(False)

ctk.CTkLabel(
    right,
    text="Activity Logs",
    font=("Segoe UI", 22, "bold")
).pack(pady=15)

log_box = ctk.CTkTextbox(right)
log_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

refresh_logs()
status_var.set("Ready")
app.mainloop()
