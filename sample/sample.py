# sample.py
# pylint: disable=E1102
from tkinter import Label, Tk

from treeviewex import TreeviewEx

root = Tk()
root.title("TreeviewEx Context Menu Demo")

status = Label(
    root,
    text=(
        "Right-click parent rows to open the built-in menu; "
        "double-click leaf cells to edit them."
    ),
)
status.pack(fill="x", padx=8, pady=(8, 4))

treeview_ex = TreeviewEx(root)
treeview_ex.pack(fill="both", expand=True, padx=8, pady=(0, 8))

columns = ("status", "owner", "notes")
treeview_ex["columns"] = columns
treeview_ex.heading("#0", text="Project", anchor="w")
treeview_ex.column("#0", width=220, stretch=False)
for col in columns:
    treeview_ex.heading(col, text=col.capitalize())
    treeview_ex.column(col, width=150)

# Demo data with nested rows so the popup menu can be tested visually.
project1 = treeview_ex.insert(
    "",
    "end",
    iid="project1",
    text="Alpha Project",
    values=("Active", "Alice", "Ready for review"),
    open=True,
)
phase1 = treeview_ex.insert(
    project1,
    "end",
    iid="project1_phase1",
    text="Phase 1",
    values=("In progress", "Alice", "Requirements and design"),
    open=True,
)
treeview_ex.insert(
    phase1,
    "end",
    iid="project1_task1",
    text="Task 1",
    values=("Open", "Alice", "Gather requirements"),
)
treeview_ex.insert(
    phase1,
    "end",
    iid="project1_task2",
    text="Task 2",
    values=("In progress", "Bob", "Implement UI"),
)

project2 = treeview_ex.insert(
    "",
    "end",
    iid="project2",
    text="Beta Project",
    values=("Planning", "Carol", "Waiting for approval"),
    open=False,
)
phase2 = treeview_ex.insert(
    project2,
    "end",
    iid="project2_phase1",
    text="Phase A",
    values=("Queued", "David", "Review spec"),
    open=False,
)
treeview_ex.insert(
    phase2,
    "end",
    iid="project2_task1",
    text="Task A",
    values=("Queued", "David", "Review spec"),
)

# The TreeviewEx context menu is built in and works without extra app code.
# Right-click a parent row to test:
# expand/collapse and recursive expand/collapse.
# Double-click a leaf cell to edit its value.
root.geometry("720x420")
root.mainloop()
