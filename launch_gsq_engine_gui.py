"""
Guitar-String-Quartet Engine GUI Launcher
Uses Tkinter only. No external dependencies.
Repo root = folder containing this script (from __file__), not shell cwd.
"""
import os
import tkinter as tk
from tkinter import messagebox

# Repo root = folder containing this script (robust for nested paths)
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Required paths for startup validation
REQUIRED_PATHS = [
    ("prompts/master-composition-engine.md", "file"),
    ("README.md", "file"),
    ("compositions", "dir"),
    ("rules", "dir"),
    ("prompts", "dir"),
    ("references", "dir"),
    ("scratch", "dir"),
]


def validate_repo_root() -> list:
    """Return list of missing paths. Empty if all present."""
    missing = []
    for path, kind in REQUIRED_PATHS:
        full = os.path.join(REPO_ROOT, path)
        if kind == "file" and not os.path.isfile(full):
            missing.append(path)
        elif kind == "dir" and not os.path.isdir(full):
            missing.append(path)
    return missing


def open_file(path: str, status_label: tk.Label) -> None:
    """Open file with default app. Show error if missing."""
    full_path = os.path.join(REPO_ROOT, path)
    if os.path.isfile(full_path):
        os.startfile(full_path)
        status_label.config(text=f"Opened: {path}")
    else:
        messagebox.showerror("File not found", f"File not found:\n{path}")
        status_label.config(text=f"Error: {path} not found")


def open_folder(path: str, status_label: tk.Label) -> None:
    """Open folder in Explorer. Show error if missing."""
    full_path = os.path.join(REPO_ROOT, path)
    if os.path.isdir(full_path):
        os.startfile(full_path)
        status_label.config(text=f"Opened: {path}")
    else:
        messagebox.showerror("Folder not found", f"Folder not found:\n{path}")
        status_label.config(text=f"Error: {path} not found")


def create_current_request(status_label: tk.Label) -> None:
    """Create current-engine-request.md from template, then open it."""
    template_path = os.path.join(REPO_ROOT, "current-engine-request-template.md")
    output_path = os.path.join(REPO_ROOT, "current-engine-request.md")

    if not os.path.isfile(template_path):
        messagebox.showerror("Template missing", "current-engine-request-template.md not found.")
        status_label.config(text="Error: template not found")
        return

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.startfile(output_path)
        status_label.config(text="Created and opened: current-engine-request.md")
        messagebox.showinfo("Success", "current-engine-request.md created and opened.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text=f"Error: {e}")


def main():
    # Startup validation
    missing = validate_repo_root()
    if missing:
        msg = "Missing paths (repository may be incomplete or launcher in wrong folder):\n\n" + "\n".join(missing)
        messagebox.showerror("Launcher validation failed", msg)
        return

    root = tk.Tk()
    root.title("Launch Guitar-String-Quartet Engine")
    root.resizable(False, False)

    # Main frame with padding
    main_frame = tk.Frame(root, padx=24, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title
    title_label = tk.Label(main_frame, text="Guitar-String-Quartet Composition Engine", font=("Segoe UI", 14, "bold"))
    title_label.pack(pady=(0, 4))

    sub_label = tk.Label(main_frame, text="Menu launcher for the master composition engine", font=("Segoe UI", 9), fg="gray")
    sub_label.pack(pady=(0, 8))

    # Repository root status
    root_label = tk.Label(main_frame, text=f"Repository root: {REPO_ROOT}", font=("Segoe UI", 8), fg="gray", anchor="w", wraplength=400)
    root_label.pack(pady=(0, 12))

    # Buttons frame
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(fill=tk.X)

    status_label = tk.Label(main_frame, text="Ready", font=("Segoe UI", 9), fg="gray", anchor="w")
    status_label.pack(fill=tk.X, pady=(16, 0))

    # Button config
    btn_pady = 4
    btn_width = 28

    def mk_file_btn(text: str, path: str):
        def cmd():
            open_file(path, status_label)
        return tk.Button(btn_frame, text=text, width=btn_width, command=cmd, padx=8, pady=4)

    def mk_folder_btn(text: str, path: str):
        def cmd():
            open_folder(path, status_label)
        return tk.Button(btn_frame, text=text, width=btn_width, command=cmd, padx=8, pady=4)

    # Buttons
    mk_file_btn("Open Master Engine Prompt", "prompts/master-composition-engine.md").pack(pady=btn_pady)
    mk_file_btn("Open Repo README", "README.md").pack(pady=btn_pady)
    mk_file_btn("Open Composition Index", "compositions/_index.md").pack(pady=btn_pady)

    create_btn = tk.Button(btn_frame, text="Create Current Engine Request", width=btn_width, padx=8, pady=4,
                           command=lambda: create_current_request(status_label))
    create_btn.pack(pady=btn_pady)

    mk_file_btn("Open Request Templates", "engine-request-templates.txt").pack(pady=btn_pady)
    mk_folder_btn("Open Compositions Folder", "compositions").pack(pady=btn_pady)
    mk_folder_btn("Open Rules Folder", "rules").pack(pady=btn_pady)
    mk_folder_btn("Open Prompts Folder", "prompts").pack(pady=btn_pady)
    mk_folder_btn("Open References Folder", "references").pack(pady=btn_pady)
    mk_folder_btn("Open Scratch Folder", "scratch").pack(pady=btn_pady)

    tk.Button(btn_frame, text="Exit", width=btn_width, command=root.quit, padx=8, pady=4).pack(pady=(12, 0))

    root.mainloop()


if __name__ == "__main__":
    main()
