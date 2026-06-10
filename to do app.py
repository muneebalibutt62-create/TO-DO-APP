import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ================= DATA =================
Data = {
    "tasks": []
}

# ================= LOAD/SAVE =================
def load_data():
    global Data
    try:
        with open("tasks.json", "r") as f:
            Data = json.load(f)
    except:
        Data = {"tasks": []}

def save_data():
    with open("tasks.json", "w") as f:
        json.dump(Data, f)

# ================= ADD TASK =================
def add_task():
    task = task_entry.get().strip()
    category = category_var.get()
    priority = priority_var.get()
    due = due_entry.get().strip()

    if task == "":
        messagebox.showerror("Error", "Enter a task")
        return

    if due == "":
        due = "No date"

    Data["tasks"].append({
        "text": task,
        "done": False,
        "priority": priority,
        "category": category,
        "due": due
    })

    save_data()
    update_ui()

    task_entry.delete(0, tk.END)
    search_var.set("")

# ================= TOGGLE DONE =================
def toggle_done(event):
    index = get_real_index(task_list.curselection()[0])
    if index is None:
        return

    Data["tasks"][index]["done"] = not Data["tasks"][index]["done"]
    save_data()
    update_ui()

# ================= DELETE =================
def delete_task():
    sel = task_list.curselection()
    if not sel:
        return

    index = get_real_index(sel[0])
    Data["tasks"].pop(index)

    save_data()
    update_ui()

# ================= SEARCH =================
def matches_search(task):
    q = search_var.get().lower()
    if q == "":
        return True
    return q in task["text"].lower()

# ================= GET INDEX =================
def get_real_index(display_index):
    visible = []

    for i, t in enumerate(Data["tasks"]):
        if not t["done"] and matches_search(t):
            visible.append(i)

    for i, t in enumerate(Data["tasks"]):
        if t["done"] and matches_search(t):
            visible.append(i)

    if display_index >= len(visible):
        return None

    return visible[display_index]

# ================= UPDATE UI =================
def update_ui():
    task_list.delete(0, tk.END)

    filtered = [t for t in Data["tasks"] if matches_search(t)]

    total = len(filtered)
    done = len([t for t in filtered if t["done"]])

    progress = 0
    if total > 0:
        progress = int((done / total) * 100)

    progress_label.config(text=f"Progress: {progress}%")

    task_list.insert(tk.END, "---- PENDING ----")

    for t in filtered:
        if not t["done"]:
            task_list.insert(
                tk.END,
                f"[{t['priority']}] [{t['category']}] {t['text']} (Due: {t['due']})"
            )

    task_list.insert(tk.END, "")
    task_list.insert(tk.END, "---- COMPLETED ----")

    for t in filtered:
        if t["done"]:
            task_list.insert(
                tk.END,
                f"✓ [{t['priority']}] [{t['category']}] {t['text']} (Due: {t['due']})"
            )

# ================= APP =================
load_data()

root = tk.Tk()
root.title("To-Do App Pro MAX")
root.geometry("550x700")
root.config(bg="#1e1e1e")

# ================= SEARCH =================
search_var = tk.StringVar()

tk.Entry(root, textvariable=search_var, bg="#2b2b2b", fg="white", insertbackground="white").pack(pady=5)

tk.Button(root, text="Search", command=update_ui, bg="#3a3a3a", fg="white").pack()

# ================= TASK INPUT =================
task_entry = tk.Entry(root, width=40, bg="#2b2b2b", fg="white", insertbackground="white")
task_entry.pack(pady=5)

due_entry = tk.Entry(root, width=40, bg="#2b2b2b", fg="white", insertbackground="white")
due_entry.insert(0, "YYYY-MM-DD")
due_entry.pack()

# ================= DROPDOWNS =================
category_var = tk.StringVar(value="Work")
priority_var = tk.StringVar(value="Medium")

tk.OptionMenu(root, category_var, "Work", "Study", "Personal").pack()
tk.OptionMenu(root, priority_var, "High", "Medium", "Low").pack()

# ================= BUTTON =================
tk.Button(root, text="Add Task", command=add_task, bg="#3a3a3a", fg="white").pack(pady=5)

# ================= PROGRESS =================
progress_label = tk.Label(root, text="Progress: 0%", fg="white", bg="#1e1e1e")
progress_label.pack()

# ================= LIST =================
task_list = tk.Listbox(
    root,
    width=70,
    height=25,
    bg="#2b2b2b",
    fg="white",
    selectbackground="#444"
)
task_list.pack(pady=10)

# ================= DELETE =================
tk.Button(root, text="Delete Task", command=delete_task, bg="red", fg="white").pack()

# ================= EVENTS =================
task_list.bind("<Double-Button-1>", toggle_done)

# ================= START =================
update_ui()
root.mainloop()