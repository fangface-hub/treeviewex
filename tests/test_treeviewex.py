import sys
import unittest
from pathlib import Path
from tkinter import Event, TclError, Tk
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from treeviewex import CellType, TreeviewEx


def _can_use_tk():
    try:
        Tk()
    except (TclError, OSError):
        return False
    return True


class TestTreeviewEx(unittest.TestCase):
    def setUp(self):
        if not _can_use_tk():
            self.skipTest("Tk is not available in this environment")
        self.root = Tk()
        self.root.withdraw()
        self.treeview_ex = TreeviewEx(self.root)
        self.treeview_ex["columns"] = ("#1", "#2", "#3")
        for col in self.treeview_ex["columns"]:
            self.treeview_ex.heading(col, text=col)
            self.treeview_ex.column(col, width=100)

        self.treeview_ex.insert(
            "", "end", iid="row1", values=("A1", "B1", "C1")
        )
        self.treeview_ex.insert(
            "", "end", iid="row2", values=("A2", "B2", "C2")
        )

        def _fake_bbox(item, column=None):
            _ = item
            _ = column
            return (0, 0, 100, 20)

        self.treeview_ex.bbox = _fake_bbox
        self.treeview_ex.entry = MagicMock()
        self.entry_value = "A1"
        self.treeview_ex.entry.get = MagicMock(
            side_effect=lambda: self.entry_value
        )
        self.treeview_ex.entry.insert = MagicMock(
            side_effect=self._mock_entry_insert
        )
        self.treeview_ex.entry.winfo_ismapped = MagicMock(return_value=False)
        self.treeview_ex.exists = MagicMock(
            side_effect=lambda row_id: row_id == "row1"
        )

    def _mock_entry_insert(self, index, value):
        if index == 0:
            self.entry_value = value

    def tearDown(self):
        self.root.destroy()

    def test_get_clicked_cell_id_pair(self):
        event = Event()
        event.x = 50
        event.y = 20
        cell_id_pair = self.treeview_ex.get_clicked_cell_id_pair(event)
        self.assertEqual(cell_id_pair, ("", ""))

    def test_get_cell_value(self):
        cell_value = self.treeview_ex.get_cell_value(("row1", "#1"))
        self.assertEqual(cell_value, "A1")

    def test_start_edit(self):
        self.treeview_ex["columns"] = ("#1", "#2", "#3")
        self.treeview_ex.start_edit(("row1", "#1"))
        self.assertEqual(self.treeview_ex._editing_cell, ("row1", "#1"))
        self.assertEqual(self.treeview_ex.entry.get(), "A1")

        with self.assertRaises(ValueError):
            self.treeview_ex.start_edit(("invalid_row", "#1"))

        with self.assertRaises(ValueError):
            self.treeview_ex.start_edit(("row1", "#99"))

        with self.assertRaises(ValueError):
            self.treeview_ex.start_edit(("row1", "invalid_column"))

        self.treeview_ex.bbox = lambda item, column=None: ""
        with self.assertRaises(ValueError):
            self.treeview_ex.start_edit(("row1", "#1"))

    def test_update_cell(self):
        self.treeview_ex.start_edit(("row1", "#1"))
        self.treeview_ex.entry.insert(0, "Updated")
        self.treeview_ex.update_cell(("row1", "#1"), self.treeview_ex.entry)
        updated_value = self.treeview_ex.get_cell_value(("row1", "#1"))
        self.assertEqual(updated_value, "Updated")

    def test_context_menu_selects_clicked_item_and_shows_popup(self):
        self.treeview_ex.insert(
            "", "end", iid="parent", values=("P1", "P2", "P3")
        )
        self.treeview_ex.insert(
            "parent",
            "end",
            iid="child_row",
            values=("C1", "C2", "C3"),
        )

        event = Event()
        event.x = 20
        event.y = 20
        event.x_root = 100
        event.y_root = 200

        self.treeview_ex.identify_row = MagicMock(return_value="parent")
        self.treeview_ex.selection_set = MagicMock()
        self.treeview_ex.focus = MagicMock()
        self.treeview_ex.context_menu.tk_popup = MagicMock()

        self.treeview_ex._on_right_click(event)

        self.treeview_ex.selection_set.assert_called_once_with("parent")
        self.treeview_ex.focus.assert_called_once_with("parent")
        self.treeview_ex.context_menu.tk_popup.assert_called_once_with(100, 200)

    def test_context_menu_not_shown_for_leaf_rows(self):
        event = Event()
        event.x = 20
        event.y = 20
        event.x_root = 100
        event.y_root = 200

        self.treeview_ex.identify_row = MagicMock(return_value="row1")
        self.treeview_ex.context_menu.tk_popup = MagicMock()

        self.treeview_ex._on_right_click(event)

        self.treeview_ex.context_menu.tk_popup.assert_not_called()

    def test_nested_child_edit_is_valid(self):
        self.treeview_ex.exists = MagicMock(
            side_effect=lambda row_id: row_id
            in {"row1", "row2", "parent", "child"}
        )
        self.treeview_ex.insert(
            "",
            "end",
            iid="parent",
            values=("P1", "P2", "P3"),
        )
        self.treeview_ex.insert(
            "parent",
            "end",
            iid="child",
            values=("C1", "C2", "C3"),
        )

        self.assertTrue(self.treeview_ex.is_valid_cell(("child", "#1")))
        self.treeview_ex.start_edit(("child", "#1"))
        self.assertEqual(self.treeview_ex._editing_cell, ("child", "#1"))

    def test_expand_and_collapse_descendants(self):
        self.treeview_ex.insert(
            "row1", "end", iid="child1", values=("A3", "B3", "C3")
        )
        self.treeview_ex.insert(
            "child1", "end", iid="grandchild1", values=("A4", "B4", "C4")
        )

        self.treeview_ex._expand_descendants("row1", expand=True)
        self.assertTrue(self.treeview_ex.item("row1", "open"))
        self.assertTrue(self.treeview_ex.item("child1", "open"))
        self.assertTrue(self.treeview_ex.item("grandchild1", "open"))

        self.treeview_ex._expand_descendants("row1", expand=False)
        self.assertFalse(self.treeview_ex.item("row1", "open"))
        self.assertFalse(self.treeview_ex.item("child1", "open"))
        self.assertFalse(self.treeview_ex.item("grandchild1", "open"))

    def test_update_cell_invalid_cell(self):
        with self.assertRaises(ValueError):
            self.treeview_ex.update_cell(
                ("invalid_row", "#1"), self.treeview_ex.entry
            )

    def test_cancel_edit(self):
        self.treeview_ex.start_edit(("row1", "#1"))
        self.treeview_ex.cancel_edit()
        self.assertIsNone(self.treeview_ex._editing_cell)
        self.assertFalse(self.treeview_ex.entry.winfo_ismapped())

    def test_readonly_behavior(self):
        self.treeview_ex.set_readonly_row("row1", True)
        self.assertEqual(
            self.treeview_ex._get_cell_type(("row1", "#1")), CellType.READONLY
        )

    def test_set_combobox_toggles(self):
        self.treeview_ex.set_combobox_column(
            "#1", values=["A", "B"], is_combobox=True
        )
        self.assertEqual(
            self.treeview_ex._get_cell_type(("row1", "#1")), CellType.COMBOBOX
        )
        self.treeview_ex.set_combobox_column("#1", is_combobox=False)
        self.assertEqual(
            self.treeview_ex._get_cell_type(("row1", "#1")), CellType.ENTRY
        )

    def test_on_return_updates_cell(self):
        self.treeview_ex._editing_cell = ("row1", "#1")
        self.treeview_ex.entry.get = MagicMock(return_value="Updated")
        event = MagicMock()
        event.widget = self.treeview_ex.entry
        self.treeview_ex._on_return(event)
        self.assertEqual(
            self.treeview_ex.get_cell_value(("row1", "#1")), "Updated"
        )
