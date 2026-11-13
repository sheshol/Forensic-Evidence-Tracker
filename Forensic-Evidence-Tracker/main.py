
import tkinter as tk
from database import init_db, count_records
import cases
import evidence
import investigators
import custody

# Create database
init_db()

# Main window
root = tk.Tk()
root.title("Forensic Evidence Tracker")
root.geometry("1100x700")
root.configure(bg="#F1F5F9")

# Colours
NAVY = "#1E3552"
BLUE = "#2563EB"
WHITE = "#FFFFFF"

# Sidebar
sidebar = tk.Frame(root, bg=NAVY, width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="FORENSIC\nEVIDENCE TRACKER",
    font=("Arial", 17, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=35)

# Main content
content = tk.Frame(root, bg="#F1F5F9")
content.pack(fill="both", expand=True)

tk.Label(
    content,
    text="Dashboard",
    font=("Arial", 26, "bold"),
    bg="#F1F5F9",
    fg=NAVY
).pack(anchor="w", padx=30, pady=(30, 5))

tk.Label(
    content,
    text="Digital Forensic Investigation Portal",
    font=("Arial", 11),
    bg="#F1F5F9",
    fg="grey"
).pack(anchor="w", padx=30)

# Statistics
stats = tk.Frame(content, bg="#F1F5F9")
stats.pack(fill="x", padx=20, pady=30)

for title, table, colour in [
    ("Total Cases", "cases", BLUE),
    ("Evidence Items", "evidence", "#7C3AED"),
    ("Investigators", "investigators", "#16A34A"),
    ("Custody Records", "custody", "#D97706")
]:
    card = tk.Frame(stats, bg=WHITE, padx=20, pady=20)
    card.pack(side="left", fill="both", expand=True, padx=8)

    tk.Label(card, text=title, bg=WHITE, fg="grey").pack(anchor="w")

    tk.Label(
        card,
        text=str(count_records(table)),
        font=("Arial", 27, "bold"),
        bg=WHITE,
        fg=colour
    ).pack(anchor="w", pady=8)

# Navigation buttons
tk.Label(
    sidebar,
    text="MAIN MENU",
    bg=NAVY,
    fg="#94A3B8",
    font=("Arial", 9, "bold")
).pack(anchor="w", padx=20, pady=15)

menu = [
    ("Dashboard", None),
    ("Cases", cases.open_window),
    ("Evidence", evidence.open_window),
    ("Investigators", investigators.open_window),
    ("Chain of Custody", custody.open_window)
]

for name, function in menu:

    if function:
        command = lambda f=function: f(root)
    else:
        command = lambda: None

    tk.Button(
        sidebar,
        text=name,
        command=command,
        bg=NAVY,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        padx=20,
        pady=14,
        font=("Arial", 11)
    ).pack(fill="x", padx=8)

tk.Label(
    sidebar,
    text="GCSec Digital Forensics",
    bg=NAVY,
    fg="#94A3B8"
).pack(side="bottom", pady=25)

# Start application
root.mainloop()
