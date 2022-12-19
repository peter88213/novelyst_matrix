"""A relationship matrix plugin for novelyst

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import os
import gettext
import locale
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.table_manager import TableManager

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
CURRENT_LANGUAGE = locale.getlocale()[0][:2]
try:
    t = gettext.translation('novelyst_matrix', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = _('Matrix')
PLUGIN = f'{APPLICATION} plugin v@release'


class Plugin:
    """novelyst relationship matrix plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.   
        on_quit() -- Apply changes and close the window.
        on_close() -- Apply changes and close the window.
    """
    VERSION = '@release'
    NOVELYST_API = '4.0'
    DESCRIPTION = 'A scene relationship table'
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
        self._matrixViewer = TableManager(self._ui, windowGeometry)
        self._matrixViewer.title(PLUGIN)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def on_close(self):
        """Apply changes and close the window."""
        self.on_quit()

    def on_quit(self):
        """Apply changes and close the window."""
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.on_quit()
