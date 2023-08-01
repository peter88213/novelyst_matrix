"""Provide a tkinter widget for relationship table management.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pywriter.pywriter_globals import *
from nvmatrixlib.relations_table import RelationsTable
from nvmatrixlib.node import Node
from nvmatrixlib.widgets.table_frame import TableFrame


class TableManager(tk.Toplevel):
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')

    def __init__(self, plugin, ui, **kwargs):
        self._ui = ui
        self._ui.refresh_tree()
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

        #--- Settings
        self._showArcs = tk.BooleanVar(value=kwargs['show_arcs'])
        self._showCharacters = tk.BooleanVar(value=kwargs['show_characters'])
        self._showLocations = tk.BooleanVar(value=kwargs['show_locations'])
        self._showItems = tk.BooleanVar(value=kwargs['show_items'])
        settings = tk.Frame(self)
        ttk.Checkbutton(settings, text=_('Show arcs'), variable=self._showArcs, onvalue=True, offvalue=False).pack(side='left', padx='2', pady='2')
        ttk.Checkbutton(settings, text=_('Show characters'), variable=self._showCharacters, onvalue=True, offvalue=False).pack(side='left', padx='2', pady='2')
        ttk.Checkbutton(settings, text=_('Show locations'), variable=self._showLocations, onvalue=True, offvalue=False).pack(side='left', padx='2', pady='2')
        ttk.Checkbutton(settings, text=_('Show items'), variable=self._showItems, onvalue=True, offvalue=False).pack(side='left', padx='2', pady='2')
        settings.pack(anchor='w')

        #--- Main window.
        self.mainWindow = TableFrame(self)

        #--- The Relations Table.
        Node.isModified = False
        if self._ui.novel is not None:
            self._relationsTable = RelationsTable(self.mainWindow, self._ui.novel, **self._kwargs)
            self._relationsTable.set_nodes()
        self.isOpen = True
        self.mainWindow.pack(fill='both', expand=True, padx=2, pady=2)

    def _apply_changes(self):
        if Node.isModified:
            if messagebox.askyesno(self.title(), f"{_('Apply changes')}?", parent=self):
                self._relationsTable.get_nodes()
                self._ui.isModified = True
                self._ui.refresh_tree()

    def on_quit(self, event=None):
        self._apply_changes()
        self._plugin.kwargs['show_arcs'] = self._showArcs.get()
        self._plugin.kwargs['show_characters'] = self._showCharacters.get()
        self._plugin.kwargs['show_locations'] = self._showLocations.get()
        self._plugin.kwargs['show_items'] = self._showItems.get()
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.mainWindow.destroy()
        # this is necessary for deleting the event bindings
        self.destroy()
        self.isOpen = False

