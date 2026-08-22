# python3
"""Treeview extension."""

from __future__ import annotations

from enum import Enum, auto
from tkinter import HORIZONTAL, VERTICAL, Entry, Event, Frame, Menu
from tkinter.ttk import Combobox, Scrollbar, Treeview
from typing import Callable, Union


class CellType(Enum):
    """Enum defining cell types."""

    ENTRY = auto()
    READONLY = auto()
    COMBOBOX = auto()


__all__ = ["CellType", "TreeviewEx"]


def _colid2colindex(column_id: str) -> int:
    """
    Convert a column ID to a column index.

    Parameters
    ----------
    column_id : str
        Column ID.

    Returns
    -------
    int
        Column index.

    """
    return int(column_id[1:]) - 1


class TreeviewEx(Treeview):  # pylint: disable=too-many-ancestors
    """Extended Treeview widget."""

    def __init__(self, master=None, **kwargs):
        """
        Initialize the widget.

        Parameters
        ----------
        master : widget, optional
            Parent widget. The default is None.
        **kwargs : dict
            Additional options passed to tkinter.ttk.Treeview.

        Returns
        -------
        None.

        """
        # Initialization
        self.readonly_rows = set()  # Keep read-only row IDs
        self.readonly_columns = set()  # Keep read-only column IDs
        self.readonly_cells = set()  # Keep read-only cells as (row, col)
        self.combobox_rows = set()  # Keep row IDs that use a combobox
        self.combobox_columns = set()  # Keep column IDs that use a combobox
        self.combobox_cells = set()  # Keep combobox cells as (row, col)
        self.combobox_row_values = {}  # Map row IDs to combobox value lists
        self.combobox_column_values = {}  # Map columns to combobox value lists
        self.combobox_cell_values = {}  # Map cells to combobox value lists

        # Other initialization
        self.frame = Frame(master=master)
        super().__init__(self.frame, **kwargs)

        # Create the Entry widget as a member
        self.entry = Entry(self)
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Escape>", self._on_escape)

        # Create the Combobox widget as a member
        self.combobox = Combobox(self)
        self.combobox.bind("<Return>", self._on_return)
        self.combobox.bind("<Escape>", self._on_escape)
        self.combobox.bind("<<ComboboxSelected>>", self._on_combobox_selected)

        # Create a vertical scrollbar and connect it
        self.scrollbar_y = Scrollbar(
            self.frame, orient=VERTICAL, command=self._on_scroll_y
        )
        self.configure(yscrollcommand=self.scrollbar_y.set)

        # Create a horizontal scrollbar and connect it
        self.scrollbar_x = Scrollbar(
            self.frame, orient=HORIZONTAL, command=self._on_scroll_x
        )
        self.configure(xscrollcommand=self.scrollbar_x.set)

        super().grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Set frame row/column weights to adjust the layout
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Bind additional behavior for the <Double-1> event
        self._additional_bind_double_click()

        # Bind the mouse wheel event
        self.bind("<MouseWheel>", self._on_mouse_wheel)
        super().bind("<Button-3>", self._on_right_click, add="+")

        self._context_menu_target_item = ""
        self.context_menu = self._create_context_menu()

        # Variables to keep editing state
        self._editing_cell = None
        self._editing_combobox_values = None  # Values for active combobox edit

    def _on_scroll_y(self, *args):
        """
        Handle vertical scroll events.

        Parameters
        ----------
        *args : tuple
            Scrollbar callback arguments.

        Returns
        -------
        None.

        """
        if self._editing_cell:
            self.cancel_edit()
        self.yview(*args)

    def _on_scroll_x(self, *args):
        """
        Handle horizontal scroll events.

        Parameters
        ----------
        *args : tuple
            Scrollbar callback arguments.

        Returns
        -------
        None.

        """
        if self._editing_cell:
            self.cancel_edit()
        self.xview(*args)

    def _on_mouse_wheel(self, event):
        """
        Handle mouse wheel events.

        Parameters
        ----------
        event : Event
            Mouse wheel event.

        Returns
        -------
        None.

        """
        if self._editing_cell:
            self.cancel_edit()

        # Run vertical scrolling
        self.yview_scroll(-1 * (event.delta // 120), "units")

    def _additional_bind_double_click(self):
        """
        Add a double-click handler.

        Returns
        -------
        None.

        """
        # Keep the existing <Double-1> binding and add this handler
        super().bind("<Double-1>", self._combined_handler, add="+")

    def _combined_handler(self, event: Event):
        """
        Handle double-click events.

        Parameters
        ----------
        event : Event
            Event object.

        Returns
        -------
        str or None
            "break" when editing started, to suppress the default toggle.

        """
        return self.on_double_click(event)  # Additional behavior

    def _on_right_click(self, event: Event) -> None:
        """Handle right-click events on expandable Treeview rows."""
        item_id = self.identify_row(event.y)
        if not item_id or not self.get_children(item_id):
            return

        self._context_menu_target_item = item_id
        self.selection_set(item_id)
        self.focus(item_id)
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def _expand_descendants(self, item_id: str, expand: bool = True) -> None:
        """Expand or collapse the node and all descendants."""
        self.item(item_id, open=expand)
        for child_id in self.get_children(item_id):
            self.item(child_id, open=expand)
            self._expand_descendants(child_id, expand=expand)

    def _create_context_menu(self) -> Menu:
        """Create the standard popup menu for tree items."""
        menu = Menu(self, tearoff=0)

        menu.add_command(
            label="Expand this node",
            command=self._expand_current_node,
        )
        menu.add_command(
            label="Collapse this node",
            command=self._collapse_current_node,
        )
        menu.add_separator()
        menu.add_command(
            label="Expand all children recursively",
            command=self._expand_all_children,
        )
        menu.add_command(
            label="Collapse all children recursively",
            command=self._collapse_all_children,
        )
        return menu

    def _get_context_menu_target_item(self) -> str:
        """Return the item clicked for the popup menu."""
        if self._context_menu_target_item:
            return self._context_menu_target_item
        selected = self.selection()
        if selected:
            return selected[0]
        return ""

    def _expand_current_node(self) -> None:
        """Expand the clicked item."""
        item_id = self._get_context_menu_target_item()
        if item_id:
            self.selection_set(item_id)
            self.focus(item_id)
            self.item(item_id, open=True)

    def _collapse_current_node(self) -> None:
        """Collapse the clicked item."""
        item_id = self._get_context_menu_target_item()
        if item_id:
            self.selection_set(item_id)
            self.focus(item_id)
            self.item(item_id, open=False)

    def _expand_all_children(self) -> None:
        """Expand all descendants of the clicked item."""
        item_id = self._get_context_menu_target_item()
        if item_id:
            self.selection_set(item_id)
            self.focus(item_id)
            self._expand_descendants(item_id, expand=True)

    def _collapse_all_children(self) -> None:
        """Collapse all descendants of the clicked item."""
        item_id = self._get_context_menu_target_item()
        if item_id:
            self.selection_set(item_id)
            self.focus(item_id)
            self._expand_descendants(item_id, expand=False)

    def bind(
        self,
        sequence: str | None = None,
        func: Callable | None = None,
        add: bool | None = None,
    ) -> str:
        """
        Override bind.

        Parameters
        ----------
        sequence : str, optional
            Same as the sequence argument of Treeview.bind().
        func : Callable, optional
            Same as the func argument of Treeview.bind().
        add : bool, optional
            Same as the add argument of Treeview.bind().

        Returns
        -------
        str
            Same return value as Treeview.bind().

        """
        if sequence == "<Double-1>":

            def combined_handler(event):
                result = self.on_double_click(event)
                if func:
                    func(event)
                return result

            return super().bind(sequence, combined_handler, add=add)
        if sequence == "<Button-3>":
            return super().bind(sequence, func, add=add)
        return super().bind(sequence, func, add=add)

    def pack(self, **kwargs):
        """
        Override pack.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments for pack.

        Returns
        -------
        None.

        """
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        """
        Override grid.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments for grid.

        Returns
        -------
        None.

        """
        self.frame.grid(**kwargs)

    def column(self, column: str, option=None, **kw):
        """
        Override column.

        Parameters
        ----------
        column : str
            Column ID.
        option : str, optional
            Column option. The default is None.
        **kw : dict
            Additional keyword arguments.

        Returns
        -------
        Any
            Return value from Treeview.column().

        """
        if option is None and "stretch" not in kw:
            kw["stretch"] = False
        return super().column(column, option, **kw)

    def get_clicked_cell_id_pair(self, event: Event) -> tuple:
        """
        Get the cell IDs at the clicked position.

        Parameters
        ----------
        event : Event
            Click event.

        Returns
        -------
        tuple
            Pair of (row ID, column ID).

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

    def on_double_click(self, event: Event) -> str | None:
        """
        Handle double-click action.

        Parameters
        ----------
        event : Event
            Event object.

        Returns
        -------
        str or None
            "break" when editing started, to stop the default
            expand/collapse toggle binding from also firing.

        """
        cell_id_pair = self.get_clicked_cell_id_pair(event)
        if cell_id_pair != ("", "") and self.is_valid_cell(cell_id_pair):
            if self.start_edit(cell_id_pair):
                # Give editing priority over the row expand/collapse toggle
                return "break"
        return None

    def get_cell_value(self, cell_id_pair: tuple) -> str:
        """
        Get a cell value.

        Parameters
        ----------
        cell_id_pair : tuple
            Pair of (row ID, column ID).

        Returns
        -------
        str
            Cell value.

        """
        row_id, column_id = cell_id_pair
        return self.item(row_id, "values")[_colid2colindex(column_id)]

    def start_edit(self, cell_id_pair: tuple) -> bool:
        """Start editing a cell. Returns True if editing actually started."""
        if not self.is_valid_cell(cell_id_pair):
            raise ValueError(f"Invalid cell specified: {cell_id_pair}")

        row_id, column_id = cell_id_pair

        cell_type = self._get_cell_type(cell_id_pair)

        # Skip editing when the cell is read-only
        if cell_type == CellType.READONLY:
            return False

        # Continue with edit processing
        self._editing_cell = cell_id_pair
        cell_value = self.get_cell_value(cell_id_pair)

        # Get the cell position and size
        bbox = self.bbox(row_id, column_id)
        if not bbox:
            raise ValueError(
                f"Cannot determine the position of the cell: {cell_id_pair}"
            )

        x, y, width, height = bbox

        # For combobox cells
        if cell_type == CellType.COMBOBOX:
            # Keep the current value list
            if cell_id_pair in self.combobox_cell_values:
                self._editing_combobox_values = self.combobox_cell_values[
                    cell_id_pair
                ]
            elif row_id in self.combobox_row_values:
                self._editing_combobox_values = self.combobox_row_values[row_id]
            elif column_id in self.combobox_column_values:
                self._editing_combobox_values = self.combobox_column_values[
                    column_id
                ]
            else:
                self._editing_combobox_values = []

            # Configure the Combobox widget
            self.combobox.delete(0, "end")
            self.combobox.insert(0, cell_value)
            self.combobox["values"] = self._editing_combobox_values

            self.combobox.place(x=x, y=y, width=width, height=height)
            self.combobox.focus_set()
        elif cell_type == CellType.ENTRY:
            # Configure the Entry widget
            self.entry.delete(0, "end")
            self.entry.insert(0, cell_value)
            self.entry.place(x=x, y=y, width=width, height=height)
            self.entry.focus_set()

        return True

    def is_valid_cell(self, cell_id_pair: tuple) -> bool:
        """
        Check whether a cell exists.

        Parameters
        ----------
        cell_id_pair : tuple
            Pair of (row ID, column ID).

        Returns
        -------
        bool
            True if the cell is valid, otherwise False.

        """
        row_id, column_id = cell_id_pair
        try:
            col_index = _colid2colindex(column_id)  # Convert column ID to index
        except (ValueError, IndexError):  # pragma: no cover
            return False  # pragma: no cover

        if not self.exists(row_id) or col_index >= len(self["columns"]):
            return False

        return True

    def _on_return(self, event):  # pylint: disable=unused-argument
        """Handle the <Return> event."""
        if self._editing_cell:
            widget = event.widget
            self.update_cell(self._editing_cell, widget)

    def _on_focus_out(self, event):  # pylint: disable=unused-argument
        """Handle the <FocusOut> event."""
        if self._editing_cell:
            widget = event.widget
            self.update_cell(self._editing_cell, widget)

    def _on_escape(self, event):  # pylint: disable=unused-argument
        """Handle the <Escape> event."""
        self.cancel_edit()

    def _on_combobox_selected(self, event):  # pylint: disable=unused-argument
        """Handle combobox selection events."""
        if self._editing_cell:
            widget = event.widget
            self.update_cell(self._editing_cell, widget)

    def _get_cell_type(self, cell_id_pair: tuple) -> CellType:
        """
        Determine a cell type.

        Parameters
        ----------
        cell_id_pair : tuple
            Pair of (row ID, column ID).

        Returns
        -------
        CellType
            CellType.READONLY, CellType.COMBOBOX, or CellType.ENTRY.

        """
        row_id, column_id = cell_id_pair

        # Check read-only settings
        if (
            row_id in self.readonly_rows
            or column_id in self.readonly_columns
            or cell_id_pair in self.readonly_cells
        ):
            return CellType.READONLY

        # Check combobox settings
        if (
            row_id in self.combobox_rows
            or column_id in self.combobox_columns
            or cell_id_pair in self.combobox_cells
        ):
            return CellType.COMBOBOX

        return CellType.ENTRY

    def update_cell(
        self, cell_id_pair: tuple, widget: Union[Entry, Combobox]
    ) -> None:
        """Update a cell value."""
        if not self.is_valid_cell(cell_id_pair):
            raise ValueError(f"Invalid cell specified: {cell_id_pair}")

        cell_type = self._get_cell_type(cell_id_pair)

        # Do not update when the cell is read-only
        if cell_type == CellType.READONLY:
            self.cancel_edit()
            return

        # Update value for ENTRY or COMBOBOX cells
        if cell_type == CellType.ENTRY or cell_type == CellType.COMBOBOX:
            # Get the new value
            new_value = widget.get()
            # Update only when the value changed
            if new_value != self.get_cell_value(cell_id_pair):
                values = list(self.item(cell_id_pair[0], "values"))
                col_index = _colid2colindex(cell_id_pair[1])
                values[col_index] = new_value
                self.item(cell_id_pair[0], values=values)

        self.cancel_edit()

    def cancel_edit(self):
        """
        Cancel editing.

        Returns
        -------
        None.

        """
        self.entry.place_forget()  # Hide Entry
        self.combobox.place_forget()  # Hide Combobox
        self._editing_cell = None
        self._editing_combobox_values = None

    def set_readonly_row(self, row_id: str, readonly: bool = True) -> None:
        """Set a row as read-only."""
        if readonly:
            self.readonly_rows.add(row_id)
        else:
            self.readonly_rows.discard(row_id)

    def set_readonly_column(
        self, column_id: str, readonly: bool = True
    ) -> None:
        """Set a column as read-only."""
        if readonly:
            self.readonly_columns.add(column_id)
        else:
            self.readonly_columns.discard(column_id)

    def set_readonly_cell(
        self, cell_id_pair: tuple, readonly: bool = True
    ) -> None:
        """Set a cell as read-only."""
        if readonly:
            self.readonly_cells.add(cell_id_pair)
        else:
            self.readonly_cells.discard(cell_id_pair)

    def set_combobox_row(
        self, row_id: str, values: list | None = None, is_combobox: bool = True
    ) -> None:
        """Set a row to use a combobox."""
        if is_combobox:
            self.combobox_rows.add(row_id)
            if values is not None:
                self.combobox_row_values[row_id] = values
        else:
            self.combobox_rows.discard(row_id)
            self.combobox_row_values.pop(row_id, None)

    def set_combobox_column(
        self,
        column_id: str,
        values: list | None = None,
        is_combobox: bool = True,
    ) -> None:
        """Set a column to use a combobox."""
        if is_combobox:
            self.combobox_columns.add(column_id)
            if values is not None:
                self.combobox_column_values[column_id] = values
        else:
            self.combobox_columns.discard(column_id)
            self.combobox_column_values.pop(column_id, None)

    def set_combobox_cell(
        self,
        cell_id_pair: tuple,
        values: list | None = None,
        is_combobox: bool = True,
    ) -> None:
        """Set a cell to use a combobox."""
        if is_combobox:
            self.combobox_cells.add(cell_id_pair)
            if values is not None:
                self.combobox_cell_values[cell_id_pair] = values
        else:
            self.combobox_cells.discard(cell_id_pair)
            self.combobox_cell_values.pop(cell_id_pair, None)
