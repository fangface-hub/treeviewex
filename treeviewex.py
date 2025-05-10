# python3
"""Treeview拡張版."""
from typing import Callable
from tkinter import (
    Frame,
    Entry,
    VERTICAL,
    HORIZONTAL,
    Event,
)
from tkinter.ttk import Treeview, Scrollbar


def _colid2colindex(column_id: str) -> int:
    """
    列IDを列インデックスに変換する.

    Parameters
    ----------
    column_id : str
        列ID.

    Returns
    -------
    int
        列インデックス.

    """
    return int(column_id[1:]) - 1


class TreeviewEx(Treeview):  # pylint: disable=too-many-ancestors
    """拡張TreeView."""

    def __init__(self, master=None, **kwargs):
        """
        コンストラクタ.

        Parameters
        ----------
        master : マスター, optional
            DESCRIPTION. The default is None.
        **kwargs : TYPE
            引数.

        Returns
        -------
        None.

        """
        # 初期化
        self.readonly_rows = set()  # 編集不可の行IDを保持
        self.readonly_columns = set()  # 編集不可の列IDを保持
        self.readonly_cells = set()  # 編集不可のセル (行ID, 列ID) を保持

        # その他の初期化処理
        self.frame = Frame(master=master)
        super().__init__(self.frame, **kwargs)

        # Entry ウィジェットをメンバとして作成
        self.entry = Entry(self)
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Escape>", self._on_escape)

        # 縦方向スクロールバーを作成し、Canvasに接続
        self.scrollbar_y = Scrollbar(
            self.frame, orient=VERTICAL, command=self._on_scroll_y
        )
        self.configure(yscrollcommand=self.scrollbar_y.set)

        # 横方向スクロールバーを作成し、Canvasに接続
        self.scrollbar_x = Scrollbar(
            self.frame, orient=HORIZONTAL, command=self._on_scroll_x
        )
        self.configure(xscrollcommand=self.scrollbar_x.set)

        super().grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Frameの行と列の重みを設定して、レイアウトを調整
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # <Double-1> イベントに対する追加の振る舞いをバインド
        self._additional_bind_double_click()

        # マウスホイールイベントをバインド
        self.bind("<MouseWheel>", self._on_mouse_wheel)

        # 編集中のセル情報を保持するための変数
        self._editing_cell = None

    def _on_scroll_y(self, *args):
        """
        縦スクロール時の処理.

        Parameters
        ----------
        *args : tuple
            スクロールバーの引数.

        Returns
        -------
        None.

        """
        if self._editing_cell:
            self.cancel_edit()
        self.yview(*args)

    def _on_scroll_x(self, *args):
        """
        横スクロール時の処理.

        Parameters
        ----------
        *args : tuple
            スクロールバーの引数.

        Returns
        -------
        None.

        """
        if self._editing_cell:
            self.cancel_edit()
        self.xview(*args)

    def _on_mouse_wheel(self, event):
        """
        マウスホイール操作時の処理.

        Parameters
        ----------
        event : Event
            マウスホイールイベント.

        Returns
        -------
        None.

        """
        if self._editing_cell:
            self.cancel_edit()

        # 縦スクロールを実行
        self.yview_scroll(-1 * (event.delta // 120), "units")

    def _additional_bind_double_click(self):
        """
        ダブルクリックハンドラの追加.

        Returns
        -------
        None.

        """
        # 既存の <Double-1> バインドを取得
        original_handler = super().bind("<Double-1>")
        self._original_bind_double_click = original_handler

        # メンバ関数をバインド
        super().bind("<Double-1>", self._combined_handler)

    def _combined_handler(self, event: Event):
        """
        ダブルクリック時のハンドラ.

        Parameters
        ----------
        event : Event
            イベント.

        Returns
        -------
        None.

        """
        self.on_double_click(event)  # 追加の振る舞い
        if self._original_bind_double_click:
            self._original_bind_double_click(event)  # 元の振る舞い

    def bind(
        self, sequence: str = None, func: Callable = None, add: bool = None
    ) -> str:
        """
        bindのオーバーライド.

        Parameters
        ----------
        sequence : str, optional
            Treeview.bind()のsequence引数同様. The default is None.
        func : Callable, optional
            Treeview.bind()のfunc引数同様. The default is None.
        add : bool, optional
            Treeview.bind()のadd引数同様. The default is None.

        Returns
        -------
        str
            Treeview.bind()のreturn同様.

        """
        if sequence == "<Double-1>":

            def combined_handler(event):
                self.on_double_click(event)
                if func:
                    func(event)

            return super().bind(sequence, combined_handler, add=add)
        else:
            return super().bind(sequence, func, add=add)

    def pack(self, **kwargs):
        """
        packのオーバーライド.

        Parameters
        ----------
        **kwargs : dict
            pcak引数の辞書.

        Returns
        -------
        None.

        """
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        """
        gridのオーバーライド.

        Parameters
        ----------
        **kwargs : dict
            grid引数の辞書.

        Returns
        -------
        None.

        """
        self.frame.grid(**kwargs)

    def column(self, column: str, option=None, **kw):
        """
        列生成のオーバーライド.

        Parameters
        ----------
        column : str
            列ID.
        option : str, optional
            オプション. The default is None.
        **kw : dict
            キーワード辞書.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if option is None and "stretch" not in kw:
            kw["stretch"] = False
        return super().column(column, option, **kw)

    def get_clicked_cell_id_pair(self, event: Event) -> tuple:
        """
        クリック位置のセルのID取得.

        Parameters
        ----------
        event : Event
            イベント.

        Returns
        -------
        cell_id_pair: tuple
            (行ID,列ID)のペア.

        """
        cell_id_pair = ("", "")
        region = self.identify_region(event.x, event.y)
        if region != "cell":
            return ("", "")
        cell_id_pair = (
            self.identify_row(event.y),
            self.identify_column(event.x),
        )
        return cell_id_pair

    def on_double_click(self, event: Event) -> None:
        """
        ダブルクリック.

        Parameters
        ----------
        event : Event
            イベント.

        Returns
        -------
        None.

        """
        self.start_edit(self.get_clicked_cell_id_pair(event))

    def get_cell_value(self, cell_id_pair: tuple) -> str:
        """
        セルの値取得.

        Parameters
        ----------
        cell_id_pair : tuple
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        (row_id, column_id) = cell_id_pair
        return self.item(row_id, "values")[_colid2colindex(column_id)]

    def start_edit(self, cell_id_pair: tuple) -> None:
        """セルの編集を開始."""
        if not self.is_valid_cell(cell_id_pair):
            raise ValueError(f"Invalid cell specified: {cell_id_pair}")

        row_id, column_id = cell_id_pair

        # readonly のチェック
        if (
            row_id in self.readonly_rows
            or column_id in self.readonly_columns
            or cell_id_pair in self.readonly_cells
        ):
            return  # 編集をスキップ

        # 編集処理を続行
        self._editing_cell = cell_id_pair
        cell_value = self.get_cell_value(cell_id_pair)

        # セルの位置とサイズを取得
        bbox = self.bbox(row_id, column_id)
        if not bbox:
            raise ValueError(
                f"Cannot determine the position of the cell: {cell_id_pair}"
            )

        x, y, width, height = bbox

        # Entry ウィジェットを設定
        self.entry.delete(0, "end")
        self.entry.insert(0, cell_value)
        self.entry.place(x=x, y=y, width=width, height=height)
        self.entry.focus_set()

    def is_valid_cell(self, cell_id_pair: tuple) -> bool:
        """
        セルの存在を確認する.

        Parameters
        ----------
        cell_id_pair : tuple
            (行ID, 列ID) のペア.

        Returns
        -------
        bool
            セルが有効であれば True, 無効であれば False.

        """
        row_id, column_id = cell_id_pair
        try:
            col_index = _colid2colindex(column_id)  # 列IDを列インデックスに変換
        except (ValueError, IndexError):  # pragma: no cover
            return False  # pragma: no cover

        if row_id not in self.get_children() or col_index >= len(
            self["columns"]
        ):
            return False

        return True

    def _on_return(self, event):  # pylint: disable=unused-argument
        """<Return> イベントハンドラー."""
        if self._editing_cell:
            self.update_cell(self._editing_cell, self.entry)

    def _on_focus_out(self, event):  # pylint: disable=unused-argument
        """<FocusOut> イベントハンドラー."""
        if self._editing_cell:
            self.update_cell(self._editing_cell, self.entry)

    def _on_escape(self, event):  # pylint: disable=unused-argument
        """<Escape> イベントハンドラー."""
        self.cancel_edit()

    def update_cell(self, cell_id_pair: tuple, entry: Entry) -> None:
        """セルの値を更新."""
        if not self.is_valid_cell(cell_id_pair):
            raise ValueError(f"Invalid cell specified: {cell_id_pair}")

        # 新しい値を取得
        new_value = entry.get()

        # 現在の値と異なる場合のみ更新
        if new_value != self.get_cell_value(cell_id_pair):
            values = list(self.item(cell_id_pair[0], "values"))
            col_index = _colid2colindex(cell_id_pair[1])
            values[col_index] = new_value
            self.item(cell_id_pair[0], values=values)

        self.cancel_edit()

    def cancel_edit(self):
        """
        編集中止.

        Returns
        -------
        None.

        """
        self.entry.place_forget()  # Entry を非表示にする
        self._editing_cell = None

    def set_readonly_row(self, row_id: str, readonly: bool = True) -> None:
        """行を readonly に設定."""
        if readonly:
            self.readonly_rows.add(row_id)
        else:
            self.readonly_rows.discard(row_id)

    def set_readonly_column(
        self, column_id: str, readonly: bool = True
    ) -> None:
        """列を readonly に設定."""
        if readonly:
            self.readonly_columns.add(column_id)
        else:
            self.readonly_columns.discard(column_id)

    def set_readonly_cell(
        self, cell_id_pair: tuple, readonly: bool = True
    ) -> None:
        """セルを readonly に設定."""
        if readonly:
            self.readonly_cells.add(cell_id_pair)
        else:
            self.readonly_cells.discard(cell_id_pair)
