"""Provide a tkinter widget for relationship table management.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/noveltree_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from novxlib.novx_globals import *
from nvmatrixlib.relations_table import RelationsTable
from nvmatrixlib.widgets.table_frame import TableFrame
from nvmatrixlib.node import Node


class TableManager(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, plugin, ui, **kwargs):
        self._ui = ui
        self._plugin = plugin
        self._kwargs = kwargs
        super().__init__()

        self._statusText = ''

        self.geometry(kwargs['window_geometry'])
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
        if self._ui.novel is not None:
            self._relationsTable = RelationsTable(self.mainWindow, self._ui.novel, **self._kwargs)
            self._relationsTable.set_nodes()
        self.isOpen = True
        self.mainWindow.pack(fill='both', expand=True, padx=2, pady=2)

        #--- Register the view.
        self._ui.views.append(self)

        #--- Initialize the view update mechanism.
        self._skipUpdate = False
        self.bind('<Control-Button-1>', self.on_element_change)

    def lock(self):
        """Inhibit element change."""
        Node.isLocked = True

    def on_quit(self, event=None):
        self.isOpen = False
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.mainWindow.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()

        #--- Unregister the view.
        self._ui.views.remove(self)

    def unlock(self):
        """enable element change."""
        Node.isLocked = False

    def update(self):
        """Refresh the view after changes have been made "outsides"."""
        if self.isOpen:
            if not self._skipUpdate:
                self.mainWindow.pack_forget()
                self.mainWindow.destroy()
                self.mainWindow = TableFrame(self)
                self.mainWindow.pack(fill='both', expand=True, padx=2, pady=2)
                self._relationsTable.draw_matrix(self.mainWindow)
                self._relationsTable.set_nodes()

    def on_element_change(self, event=None):
        """Update the model, but not the view."""
        self._skipUpdate = True
        self._relationsTable.get_nodes()
        self._skipUpdate = False
