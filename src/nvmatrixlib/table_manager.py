"""Provide a tkinter widget for relationship table management.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from nvmatrixlib.nvmatrix_globals import *
from ywtablelib.relations_table import RelationsTable
from ywtablelib.node import Node
from ywtablelib.scrolled_window import ScrolledWindow

SETTINGS = dict(
    last_open='',
    tree_width='300',
)
OPTIONS = {}


class TableManager(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, ui, position):
        self._ui = ui
        super().__init__()

        self.title(PLUGIN)
        self._statusText = ''

        self.geometry(position)
        self.lift()
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.bind(self._KEY_QUIT_PROGRAM[0], self.on_quit)

        #--- Main menu.
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        #--- Main window.
        self.mainWindow = ScrolledWindow(self)

        #--- The Relations Table.
        Node.isModified = False
        if self._ui.novel is not None:
            self._relationsTable = RelationsTable(self.mainWindow.display, self._ui.novel)
            self._relationsTable.set_nodes()
        self.isOpen = True
        self.mainWindow.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    def _apply_changes(self):
        if Node.isModified:
            if messagebox.askyesno(PLUGIN, f"{_('Apply changes')}?"):
                self._relationsTable.get_nodes()
                self._ui.isModified = True
                self._ui.refresh_tree()

    def on_quit(self, event=None):
        self._apply_changes()
        self.destroy()
        self.isOpen = False

