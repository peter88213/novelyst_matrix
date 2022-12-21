"""Provide a tkinter widget for relationship table management.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import messagebox
from ywtablelib.ywtable_globals import *
from ywtablelib.relations_table import RelationsTable
from ywtablelib.node import Node
from ywtablelib.table_frame import TableFrame


class TableManager(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, plugin, ui, position):
        self._ui = ui
        self._plugin = plugin
        super().__init__()

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
        self.mainWindow = TableFrame(self)

        #--- The Relations Table.
        Node.isModified = False
        if self._ui.novel is not None:
            self._relationsTable = RelationsTable(self.mainWindow, self._ui.novel)
            self._relationsTable.set_nodes()
        self.isOpen = True
        self.mainWindow.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    def _apply_changes(self):
        if Node.isModified:
            if messagebox.askyesno(self.title(), f"{_('Apply changes')}?"):
                self._relationsTable.get_nodes()
                self._ui.isModified = True
                self._ui.refresh_tree()

    def on_quit(self, event=None):
        self._apply_changes()
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

