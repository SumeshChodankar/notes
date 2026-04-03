import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os

# ---------- Setup ----------
NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

def get_today_file():
    return os.path.join(NOTES_DIR, datetime.now().strftime("%Y-%m-%d") + ".txt")

# ---------- Save ----------
def save_notes(event=None):
    content = text.get("1.0", tk.END).strip()
    if not content:
        return

    file_path = get_today_file()

    with open(file_path, "a") as f:
        f.write(f"\n=== {datetime.now().strftime('%B %d')} ===\n")
        for line in content.split("\n"):
            f.write(f"• {line}\n")

    text.delete("1.0", tk.END)
    text.insert("1.0", "• ")  # restart bullet
    status.config(text="Saved ✔ (Ctrl+S)")

# ---------- Toggle ----------
def toggle_window():
    if root.state() == "normal":
        root.withdraw()
    else:
        root.deiconify()

# ---------- Search ----------
def search_notes():
    keyword = search_entry.get().lower()
    results.delete("1.0", tk.END)

    found = False

    for file in os.listdir(NOTES_DIR):
        path = os.path.join(NOTES_DIR, file)

        with open(path, "r") as f:
            for line in f:
                if keyword in line.lower():
                    results.insert(tk.END, f"{file}: {line}")
                    found = True

    if not found:
        results.insert(tk.END, "No results found.")

# ---------- Smart Enter ----------
def handle_enter(event):
    current_line = text.get("insert linestart", "insert")

    if current_line.strip().startswith("•"):
        text.insert("insert", "\n• ")
        return "break"

    elif current_line.strip().startswith("[ ]"):
        text.insert("insert", "\n[ ] ")
        return "break"

# ---------- UI ----------
root = tk.Tk()
root.title("Todo List")
root.geometry("380x520")
root.configure(bg="#1e1e1e")
root.attributes("-topmost", True)

# ---------- Header ----------
header = tk.Frame(root, bg="#2b2b2b", height=40)
header.pack(fill="x")

title = tk.Label(header, text="📝 Todo List", fg="white", bg="#2b2b2b", font=("Segoe UI", 12, "bold"))
title.pack(side="left", padx=10, pady=5)

date_label = tk.Label(
    header,
    text=datetime.now().strftime("%b %d"),
    fg="#aaaaaa",
    bg="#2b2b2b",
    font=("Segoe UI", 9)
)
date_label.pack(side="right", padx=10)

# ---------- Editor ----------
text = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    bg="#252526",
    fg="#4FD1C5",  # aqua blue
    insertbackground="#4FD1C5",
    font=("Segoe UI", 11),
    spacing1=4,
    spacing3=4,
    padx=12,
    pady=12,
    relief="flat"
)
text.pack(fill="both", expand=True, padx=10, pady=(10, 5))

# Start with bullet
text.insert("1.0", "• ")

# Bindings
text.bind("<Return>", handle_enter)
root.bind("<Control-s>", save_notes)

# ---------- Buttons ----------
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(fill="x", padx=10, pady=5)

save_btn = tk.Button(
    btn_frame,
    text="💾 Save",
    command=save_notes,
    bg="#007acc",
    fg="white",
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=8
)
save_btn.pack(side="left", padx=5)

hide_btn = tk.Button(
    btn_frame,
    text="Hide",
    command=toggle_window,
    bg="#3a3a3a",
    fg="white",
    relief="flat",
    padx=15,
    pady=8
)
hide_btn.pack(side="right", padx=5)

# ---------- Search ----------
search_frame = tk.Frame(root, bg="#1e1e1e")
search_frame.pack(fill="x", padx=10, pady=(5, 0))

search_entry = tk.Entry(
    search_frame,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white",
    relief="flat"
)
search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=4)

search_btn = tk.Button(
    search_frame,
    text="Search",
    command=search_notes,
    bg="#3a3a3a",
    fg="white",
    relief="flat",
    padx=10
)
search_btn.pack(side="right")

# ---------- Results ----------
results = scrolledtext.ScrolledText(
    root,
    height=8,
    bg="#111",
    fg="#4FD1C5",  # aqua
    insertbackground="#4FD1C5",
    font=("Consolas", 9),
    relief="flat",
    padx=10,
    pady=10
)
results.pack(fill="both", padx=10, pady=5)

# ---------- Status ----------
status = tk.Label(
    root,
    text="Ready",
    bg="#1e1e1e",
    fg="#888",
    font=("Segoe UI", 8)
)
status.pack(pady=(0, 5))

root.mainloop()