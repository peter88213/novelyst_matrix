"""Provide a tkinter widget for project matrix management.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from novelystlib.widgets.text_box import TextBox
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.matrix import Matrix
from nvmatrixlib.configuration import Configuration

SETTINGS = dict(
    last_open='',
    tree_width='300',
)
OPTIONS = {}


class MatrixTk(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, ui, position, configDir):
        self._ui = ui
        super().__init__()

        #--- Load configuration.
        self.iniFile = f'{configDir}/matrix.ini'
        self.configuration = Configuration(SETTINGS, OPTIONS)
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        # Read the file path from the configuration file.

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
        if self._ui.novel is not None:
            self._matrix = Matrix(self.mainWindow, self._ui.novel)

    #--- Application related methods.

    def on_quit(self, event=None):

        #--- Save project specific configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)
        self.destroy()
        self.isOpen = False
