"""A relationship matrix plugin for novelyst

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.matrix_tk import MatrixTk


class Plugin:
    """novelyst relationship matrix plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.    
    """
    VERSION = '@release'
    NOVELYST_API = '4.0'
    DESCRIPTION = 'A relationship matrix'
    URL = 'https://peter88213.github.io/novelyst_matrix'

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        self._matrixViewer = None

        # Create a submenu
        self._ui.toolsMenu.insert_command(0, label=APPLICATION, command=self._start_ui)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def _start_ui(self):
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.lift()
                self._matrixViewer.focus()
                return

        __, x, y = self._ui.root.geometry().split('+')
        offset = 100
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        self._matrixViewer = MatrixTk(self._ui, windowGeometry)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def on_quit(self):
        """Write back the configuration file."""
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.on_quit()
