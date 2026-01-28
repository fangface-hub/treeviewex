# sample.py
# pylint: disable=E1102
from tkinter import Tk

from treeviewex import TreeviewEx

# 使用例(Usage Example)
root = Tk()
root.title("TreeviewEx Example")

# TreeviewExを配置(Place TreeviewEx)
treeview_ex = TreeviewEx(root)
treeview_ex.grid(row=0, column=0, sticky="nsew")

# Treeviewの列を設定(Set Treeview columns)
columns = ("col1", "col2", "col3", "col4")
treeview_ex["columns"] = columns
treeview_ex.heading("#0", text="", anchor="w")
treeview_ex.column("#0", width=0, stretch=False)
for col in columns:
    treeview_ex.heading(col, text=f"{col.capitalize()}")
    # 各列の幅を手動で設定(Manually set the width of each column)
    treeview_ex.column(col, width=100)

# テストデータを追加(Add test data)
for i in range(100):
    treeview_ex.insert(
        "",
        "end",
        text="",
        values=(f"Value {i}A", f"Value {i}B", f"Value {i}C", f"Value {i}D"),
    )

# readonlyの設定(Readonly settings)
# 行をreadonlyに設定(Set a row to readonly)
treeview_ex.set_readonly_row(row_id="I002", readonly=True)
# 列をreadonlyに設定(Set a column to readonly)
treeview_ex.set_readonly_column(column_id="#2", readonly=True)
treeview_ex.set_readonly_cell(
    cell_id_pair=("I003", "#3"),
    readonly=True)  # セルをreadonlyに設定(Set a cell to readonly)

# comboboxの設定(Combobox settings)
# 行をcomboboxに設定(Set a row to combobox)
treeview_ex.set_combobox_row(
    row_id="I004",
    values=["Row Option A", "Row Option B", "Row Option C"],
    is_combobox=True)
# 列をcomboboxに設定(Set a column to combobox)
treeview_ex.set_combobox_column(
    column_id="#1",
    values=["Col Option A", "Col Option B", "Col Option C"],
    is_combobox=True)
# セルをcomboboxに設定(Set a cell to combobox with specific values)
treeview_ex.set_combobox_cell(
    cell_id_pair=("I005", "#3"),
    values=["Option A", "Option B", "Option C", "Option D"],
    is_combobox=True)

# Frameの行と列の重みを設定して、レイアウトを調整
# (Adjust the layout by setting row and column
#  weights for the frame)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
