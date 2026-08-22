# TreeviewEx

[日本語](README_ja.md)

Treeview extension for Tkinter.

This package adds the following features to the standard tkinter Treeview:

- Vertical and horizontal scroll bars
- Cell editing
- Read-only settings for rows, columns, and cells

All other behavior is the same as the standard tkinter Treeview.

---

## Testing

1. Install dependencies

   ```bash
   uv sync --group dev
   ```

2. Run the tests

   ```bash
   uv run pytest -q
   ```

3. Show coverage report

   ```bash
   uv run coverage run -m pytest -q
   uv run coverage report -m
   ```

4. Generate an HTML report (optional)

   ```bash
   uv run coverage html
   ```

---

## Build

1. Install dependencies

   ```bash
   uv sync --group dev
   ```

2. Build the package

   ```bash
   uv build
   ```

3. Check the generated wheel in the dist folder

---

## Usage

1. Install the package

   ```bash
   uv pip install path/to/TreeviewEx.whl
   ```

2. Run the sample

   ```bash
   uv run python sample/sample.py
   ```

Simple example without nested rows:

```python
from tkinter import Tk
from treeviewex import TreeviewEx

root = Tk()
root.title("TreeviewEx Simple Example")

treeview_ex = TreeviewEx(root)
treeview_ex.pack(fill="both", expand=True)

treeview_ex["columns"] = ("status", "owner", "notes")
treeview_ex.heading("#0", text="Task", anchor="w")
treeview_ex.column("#0", width=120, stretch=False)
for col in treeview_ex["columns"]:
    treeview_ex.heading(col, text=col.capitalize())
    treeview_ex.column(col, width=150)

treeview_ex.insert(
    "",
    "end",
    iid="task1",
    text="Task 1",
    values=("Open", "Alice", "Gather requirements"),
)
treeview_ex.insert(
    "",
    "end",
    iid="task2",
    text="Task 2",
    values=("In progress", "Bob", "Implement UI"),
)
treeview_ex.insert(
    "",
    "end",
    iid="task3",
    text="Task 3",
    values=("Done", "Carol", "Review spec"),
)

root.geometry("600x200")
root.mainloop()
```

Double-click a cell to edit its value. Since there are no child rows, double-clicking never toggles expand/collapse.

Example with a built-in context menu:

```python
from tkinter import Tk
from treeviewex import TreeviewEx

root = Tk()
root.title("TreeviewEx Context Menu Demo")

# No custom popup code is needed. TreeviewEx automatically binds the
# right-click menu to each visible item.
treeview_ex = TreeviewEx(root)
treeview_ex.pack(fill="both", expand=True)

treeview_ex["columns"] = ("status", "owner", "notes")
treeview_ex.heading("#0", text="Project", anchor="w")
treeview_ex.column("#0", width=220, stretch=False)
for col in treeview_ex["columns"]:
    treeview_ex.heading(col, text=col.capitalize())
    treeview_ex.column(col, width=150)

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

root.geometry("700x400")
root.mainloop()
```

Right-click a parent row with children to test the built-in menu actions: expand, collapse, and recursive expand/collapse. Leaf rows do not show the popup menu; double-click their cells to edit values.

---

## Public interfaces

### set_readonly_row(row_id: str, readonly: bool = True) -> None

Set the specified row to readonly.

### set_readonly_column(column_id: str, readonly: bool = True) -> None

Set the specified column to readonly.

### set_readonly_cell(cell_id_pair: tuple, readonly: bool = True) -> None

Set the specified cell to readonly.

### set_combobox_row(row_id: str, values: list = None, is_combobox: bool = True) -> None

Set the specified row to be editable with a Combobox.

### set_combobox_column(column_id: str, values: list = None, is_combobox: bool = True) -> None

Set the specified column to be editable with a Combobox.

### set_combobox_cell(cell_id_pair: tuple, values: list = None, is_combobox: bool = True) -> None

Set the specified cell to be editable with a Combobox.

---

## License

This project is licensed under the MIT License.
