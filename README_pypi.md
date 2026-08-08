# TreeviewEx

TreeviewEx is a lightweight extension for Tkinter's built-in Treeview widget.

It adds useful editing features while keeping the standard Treeview behavior intact.

## Features

- Vertical and horizontal scrollbars
- Cell editing
- Read-only support for rows, columns, and cells
- Combobox-style editing for rows, columns, and cells

## Installation

```bash
pip install treeviewex
```

## Quick example

```python
from tkinter import Tk
from treeviewex import TreeviewEx

root = Tk()
root.title("TreeviewEx Example")

treeview_ex = TreeviewEx(root)
treeview_ex.grid(row=0, column=0, sticky="nsew")

columns = ("col1", "col2", "col3")
treeview_ex["columns"] = columns
treeview_ex.heading("#0", text="", anchor="w")
treeview_ex.column("#0", width=0, stretch=False)

for col in columns:
    treeview_ex.heading(col, text=col.capitalize())
    treeview_ex.column(col, width=120)

for i in range(5):
    treeview_ex.insert(
        "",
        "end",
        text="",
        values=(f"Value {i}A", f"Value {i}B", f"Value {i}C"),
    )

root.mainloop()
```

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

## License

This project is licensed under the MIT License.
