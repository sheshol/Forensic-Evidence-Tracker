
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB = "forensic.db"

TABLES = {
    "cases": ["case_id", "case_name", "client", "priority", "status"],
    "evidence": ["evidence_id", "case_id", "evidence_type", "description", "location", "status"],
    "investigators": ["investigator_id", "name", "specialisation", "email"],
    "custody": ["record_id", "evidence_id", "handled_by", "action", "record_date"]
}

def connect():
    return sqlite3.connect(DB)

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY, case_name TEXT, client TEXT,
            priority TEXT, status TEXT)""")

        con.execute("""CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT PRIMARY KEY, case_id TEXT, evidence_type TEXT,
            description TEXT, location TEXT, status TEXT)""")

        con.execute("""CREATE TABLE IF NOT EXISTS investigators (
            investigator_id TEXT PRIMARY KEY, name TEXT,
            specialisation TEXT, email TEXT)""")

        con.execute("""CREATE TABLE IF NOT EXISTS custody (
            record_id TEXT PRIMARY KEY, evidence_id TEXT,
            handled_by TEXT, action TEXT, record_date TEXT)""")

def add_record(table, values):
    columns = TABLES[table]
    with connect() as con:
        con.execute(
            f"INSERT INTO {table} VALUES ({','.join(['?'] * len(columns))})",
            values
        )

def get_records(table):
    with connect() as con:
        return con.execute(f"SELECT * FROM {table}").fetchall()

def delete_record(table, record_id):
    with connect() as con:
        con.execute(
            f"DELETE FROM {table} WHERE {TABLES[table][0]} = ?",
            (record_id,)
        )

def count_records(table):
    with connect() as con:
        return con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

def open_manager(parent, title, table):
    fields = TABLES[table]
    window = tk.Toplevel(parent)
    window.title(title)
    window.geometry("850x500")

    tk.Label(window, text=title, font=("Arial", 20, "bold")).pack(pady=15)

    form = tk.Frame(window)
    form.pack(pady=10)

    entries = []

    for i, field in enumerate(fields):
        tk.Label(form, text=field.replace("_", " ").title()).grid(row=i, column=0, padx=8, pady=5)
        entry = tk.Entry(form, width=30)
        entry.grid(row=i, column=1, padx=8, pady=5)
        entries.append(entry)

    columns = fields
    tree = ttk.Treeview(window, columns=columns, show="headings", height=8)

    for field in fields:
        tree.heading(field, text=field.replace("_", " ").title())
        tree.column(field, width=125)

    tree.pack(fill="both", expand=True, padx=15, pady=10)

    def refresh():
        tree.delete(*tree.get_children())
        for record in get_records(table):
            tree.insert("", "end", values=record)

    def save():
        values = [entry.get().strip() for entry in entries]

        if not all(values):
            messagebox.showerror("Error", "Please complete all fields.")
            return

        try:
            add_record(table, values)
            refresh()
            for entry in entries:
                entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Record saved successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This ID already exists.")

    def remove():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select record", "Select a record first.")
            return

        record = tree.item(selected[0])["values"]
        if messagebox.askyesno("Confirm", "Delete this record?"):
            delete_record(table, record[0])
            refresh()

    buttons = tk.Frame(window)
    buttons.pack(pady=10)

    tk.Button(buttons, text="Add Record", command=save,
              bg="#2563EB", fg="white", width=15).pack(side="left", padx=5)

    tk.Button(buttons, text="Delete Selected", command=remove,
              width=15).pack(side="left", padx=5)

    refresh()
