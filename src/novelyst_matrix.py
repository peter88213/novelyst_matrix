"""A project matrix manager plugin for novelyst.

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.matrix_tk import MatrixTk

DEFAULT_FILE = 'matrix.pwc'


class Plugin:
    """novelyst matrix manager plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.    
    """
    VERSION = '@release'
    NOVELYST_API = '4.0'
    DESCRIPTION = 'A book/series matrix manager'
    URL = 'https://peter88213.github.io/novelyst_matrix'

    def install(self, ui):
        """Add a submenu to the 'File' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        self._matrixViewer = None

        # Create a submenu
        self._ui.fileMenu.insert_command(0, label=APPLICATION, command=self._start_ui)
        self._ui.fileMenu.insert_separator(1)
        self._ui.fileMenu.entryconfig(APPLICATION, state='normal')

    def _start_ui(self):
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.lift()
                self._matrixViewer.focus()
                return

        __, x, y = self._ui.root.geometry().split('+')
        offset = 300
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.pywriter/novelyst/config'
        except:
            configDir = '.'
        self._matrixViewer = MatrixTk(self._ui, windowGeometry, configDir)

    def on_quit(self):
        """Write back the configuration file."""
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.on_quit()
