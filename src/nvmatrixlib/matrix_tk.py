"""Provide a tkinter widget for project matrix management.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.matrix import Matrix
from nvmatrixlib.node import Node

SETTINGS = dict(
    last_open='',
    tree_width='300',
)
OPTIONS = {}


class MatrixTk(tk.Toplevel):
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
        self.mainWindow = ttk.Frame(self)
        self.mainWindow.pack(fill=tk.BOTH, padx=2, pady=2)

        #--- The Matrix.
        Node.isModified = False
        if self._ui.novel is not None:
            self._matrix = Matrix(self.mainWindow, self._ui.novel)
            self._matrix.set_nodes()

    #--- Application related methods.

    def on_quit(self, event=None):

        #--- Apply changes.
        if Node.isModified:
            if messagebox.askyesno(PLUGIN, f"{_('Apply changes')}?"):
                self._matrix.get_nodes()
                self._ui.prjFile.write()
                self._ui.refresh_tree()

        self.destroy()
        self.isOpen = False
