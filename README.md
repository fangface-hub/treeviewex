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

Example:

```python
from treeviewex import TreeviewEx
from tkinter import Tk

root = Tk()
root.title("TreeviewEx Example")

treeview_ex = TreeviewEx(root)
treeview_ex.grid(row=0, column=0, sticky="nsew")

columns = ("col1", "col2", "col3", "col4")
treeview_ex["columns"] = columns
treeview_ex.heading("#0", text="", anchor="w")
treeview_ex.column("#0", width=0, stretch=False)
for col in columns:
    treeview_ex.heading(col, text=f"{col.capitalize()}")
    treeview_ex.column(col, width=100)

for i in range(100):
    treeview_ex.insert(
        "",
        "end",
        text="",
        values=(f"Value {i}A", f"Value {i}B", f"Value {i}C", f"Value {i}D"),
    )

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
```

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
