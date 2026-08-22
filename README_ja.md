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

1. 依存関係をインストールする<br>`Install dependencies`

    ```bash
    uv sync --extra dev
    ```

1. テストを実行する<br>`Run the tests`

    ```bash
    uv run pytest -q
    ```

1. カバレッジレポートを表示する<br>`Display the coverage report`

    ```bash
    uv run coverage run -m pytest -q
    uv run coverage report -m
    ```

1. HTML レポートを生成する（オプション）<br>`Generate an HTML report (optional)`

    ```bash
    uv run coverage html
    ```

---

## ビルド方法<br>`How to build`

1. 依存関係をインストールする<br>`Install dependencies`

    ```bash
    uv sync --extra dev
    ```

1. ビルドコマンドを打つ<br>`Run the build command`

    ```bash
    uv build
    ```

1. `dist` フォルダ内に生成された `.whl` ファイルを確認する<br>`Check the generated .whl file in the dist folder`

---

## 使用方法<br>`How to use`

1. パッケージをインストールする<br>`Install the package`

    ```bash
    uv pip install path/to/TreeviewEx.whl
    ```

1. サンプルコードを実行する<br>`Run the sample code`

    ```bash
    uv run python sample/sample.py
    ```

    折り畳みのない、シンプルなサンプル<br>`Simple example without nested rows`

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

    セルをダブルクリックすると編集できます。子行が無いため、ダブルクリックしても展開・折りたたみは発生しません。<br>`Double-click a cell to edit its value. Since there are no child rows, double-clicking never toggles expand/collapse.`

    ```python
    from tkinter import Tk
    from treeviewex import TreeviewEx

    root = Tk()
    root.title("TreeviewEx Context Menu Demo")

    # カスタムのポップアップコードは不要です。
    # TreeviewEx が自動で右クリックメニューを各ノードに割り当てます。
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

    子を持つ親ノードを右クリックすると、展開・折りたたみ、再帰的な展開/折りたたみの各メニューを試せます。リーフ行にはメニューは出ず、セルをダブルクリックすると編集できます。

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

---

## Sponsor

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/fangface-hub)
