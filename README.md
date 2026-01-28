# TreeviewEx

Treeview の拡張版<br>
`Enhanced version of Treeview`

tkinter の Treeview に以下の機能を追加<br>`Added the following features to tkinter Treeview`

* 縦横スクロールバー<br>`Vertical and horizontal scroll bars`
* セルの編集<br>`Editing a cell`
* 行、列、セルの readonly設定<br>`Readonly setting for rows, columns, and cells`

その他の機能は tkinter の Treeview と同じ<br>`Other features are the same as tkinter Treeview.`

---

## テスト方法<br>`How to test`

1. 必要なパッケージをインストールする<br>`Install required packages`

    ```bash
    pip install coverage
    ```

1. テストを実行する<br>`Run the tests`

    ```bash
    coverage run -m unittest discover
    ```

1. カバレッジレポートを表示する<br>`Display the coverage report`

    ```bash
    coverage report -m
    ```

1. HTML レポートを生成する（オプション）<br>`Generate an HTML report (optional)`

    ```bash
    coverage html
    ```

---

## ビルド方法<br>`How to build`

1. 必要なパッケージをインストールする<br>`Install required packages`

    ```bash
    pip install setuptools wheel
    ```

1. ビルドコマンドを打つ<br>`Run the build command`

    ```bash
    python setup.py bdist_wheel
    ```

1. `dist` フォルダ内に生成された `.whl` ファイルを確認する<br>`Check the generated .whl file in the dist folder`

---

## 使用方法<br>`How to use`

1. パッケージをインストールする<br>`Install the package`

    ```bash
    pip install path/to/TreeviewEx.whl
    ```

1. サンプルコードを実行する<br>`Run the sample code`

    ```python
    from treeviewex import TreeviewEx
    from tkinter import Tk

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
        readonly=True
    )  # セルをreadonlyに設定(Set a cell to readonly)

    # Frameの行と列の重みを設定して、レイアウトを調整
    # (Adjust the layout by setting row and column
    #  weights for the frame)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
    ```

---

## 公開インターフェース<br>`Public Interfaces`

以下は `TreeviewEx` クラスの主な公開インターフェースです。<br>`The following are the main public interfaces of the TreeviewEx class.`

### `set_readonly_row(row_id: str, readonly: bool = True) -> None`

指定した行を編集不可（readonly）に設定します。<br>`Set the specified row to readonly.`

* __Parameters__
  * `row_id` (`str`): 編集不可にする行の ID。<br>`The ID of the row to set as readonly.`
  * `readonly` (`bool`, optional): `True` の場合は編集不可、`False` の場合は編集可能に設定します。デフォルトは `True`。<br>`Set to True to make the row readonly, or False to make it editable. Default is True.`

* __Example__

  ```python
  treeview_ex.set_readonly_row(row_id="I002", readonly=True)
  ```

---

### `set_readonly_column(column_id: str, readonly: bool = True) -> None`

指定した列を編集不可（readonly）に設定します。<br>`Set the specified column to readonly.`

* __Parameters__
  * `column_id` (`str`): 編集不可にする列の ID。<br>`The ID of the column to set as readonly.`
  * `readonly` (`bool`, optional): `True` の場合は編集不可、`False` の場合は編集可能に設定します。デフォルトは `True`。<br>`Set to True to make the column readonly, or False to make it editable. Default is True.`

* __Example__

  ```python
  treeview_ex.set_readonly_column(column_id="#2", readonly=True)
  ```

---

### `set_readonly_cell(cell_id_pair: tuple, readonly: bool = True) -> None`

指定したセルを編集不可（readonly）に設定します。<br>`Set the specified cell to readonly.`

* __Parameters__
  * `cell_id_pair` (`tuple`): 編集不可にするセルの (行ID, 列ID) のペア。<br>`A tuple (row ID, column ID) of the cell to set as readonly.`
  * `readonly` (`bool`, optional): `True` の場合は編集不可、`False` の場合は編集可能に設定します。デフォルトは `True`。<br>`Set to True to make the cell readonly, or False to make it editable. Default is True.`

* __Example__

  ```python
  treeview_ex.set_readonly_cell(cell_id_pair=("I003", "#3"), readonly=True)
  ```

---

### `set_combobox_row(row_id: str, values: list = None, is_combobox: bool = True) -> None`

指定した行を Combobox で編集可能に設定します。<br>`Set the specified row to be editable with a Combobox.`

* __Parameters__
  * `row_id` (`str`): Combobox にする行の ID。<br>`The ID of the row to set as combobox.`
  * `values` (`list`, optional): Combobox のドロップダウンメニューに表示する値のリスト。デフォルトは `None`。<br>`A list of values to display in the Combobox dropdown menu. Default is None.`
  * `is_combobox` (`bool`, optional): `True` の場合は Combobox に設定、`False` の場合は Combobox を解除します。デフォルトは `True`。<br>`Set to True to make the row a combobox, or False to disable it. Default is True.`

* __Example__

  ```python
  treeview_ex.set_combobox_row(
      row_id="I004",
      values=["Option A", "Option B", "Option C"],
      is_combobox=True)
  ```

---

### `set_combobox_column(column_id: str, values: list = None, is_combobox: bool = True) -> None`

指定した列を Combobox で編集可能に設定します。<br>`Set the specified column to be editable with a Combobox.`

* __Parameters__
  * `column_id` (`str`): Combobox にする列の ID。<br>`The ID of the column to set as combobox.`
  * `values` (`list`, optional): Combobox のドロップダウンメニューに表示する値のリスト。デフォルトは `None`。<br>`A list of values to display in the Combobox dropdown menu. Default is None.`
  * `is_combobox` (`bool`, optional): `True` の場合は Combobox に設定、`False` の場合は Combobox を解除します。デフォルトは `True`。<br>`Set to True to make the column a combobox, or False to disable it. Default is True.`

* __Example__

  ```python
  treeview_ex.set_combobox_column(
      column_id="#1",
      values=["Option X", "Option Y", "Option Z"],
      is_combobox=True)
  ```

---

### `set_combobox_cell(cell_id_pair: tuple, values: list = None, is_combobox: bool = True) -> None`

指定したセルを Combobox で編集可能に設定します。<br>`Set the specified cell to be editable with a Combobox.`

* __Parameters__
  * `cell_id_pair` (`tuple`): Combobox にするセルの (行ID, 列ID) のペア。<br>`A tuple (row ID, column ID) of the cell to set as combobox.`
  * `values` (`list`, optional): Combobox のドロップダウンメニューに表示する値のリスト。デフォルトは `None`。<br>`A list of values to display in the Combobox dropdown menu. Default is None.`
  * `is_combobox` (`bool`, optional): `True` の場合は Combobox に設定、`False` の場合は Combobox を解除します。デフォルトは `True`。<br>`Set to True to make the cell a combobox, or False to disable it. Default is True.`

* __Example__

  ```python
  treeview_ex.set_combobox_cell(
      cell_id_pair=("I005", "#2"),
      values=["Option A", "Option B", "Option C", "Option D"],
      is_combobox=True)
  ```

---

## ライセンス<br>`License`

このプロジェクトは MIT ライセンスの下で公開されています。<br>
`This project is licensed under the MIT License.`
