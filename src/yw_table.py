"""A relationship table for yw7 files

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import tkinter as tk
from tkinter import messagebox
from pywriter.ui.main_tk import MainTk
from nvmatrixlib.nvmatrix_globals import *
from ywtablelib.relations_table import RelationsTable
from ywtablelib.node import Node
from ywtablelib.scrolled_window import ScrolledWindow

APPLICATION = 'Relationship Table'


class TableManager(MainTk):

    def __init__(self):
        kwargs = {
                'root_geometry': '',
                'yw_last_open': '',
                'color_text_bg':'white',
                'color_text_fg':'black',
                }
        super().__init__(APPLICATION, **kwargs)
        # self.root.state('zoom')
        # self.mainWindow.pack_propagate(0)

    def open_project(self, fileName):
        super().open_project(fileName)
        #--- The Relationship Table.
        Node.isModified = False
        if self.novel is not None:
            self._tableWindow = ScrolledWindow(self.mainWindow)
            self._relationsTable = RelationsTable(self._tableWindow.display, self.novel)
            self._tableWindow.pack(fill=tk.BOTH, expand=True)
            self._relationsTable.set_nodes()

    def close_project(self, event=None):
        self._apply_changes()
        self._relationsTable = None
        self._tableWindow.destroy()
        super().close_project()

    def on_quit(self, event=None):
        self._apply_changes()
        super().on_quit()

    def _apply_changes(self):
        #--- Apply changes.
        if Node.isModified:
            if messagebox.askyesno(PLUGIN, f"{_('Apply changes')}?"):
                self._relationsTable.get_nodes()
                self.prjFile.write()
            Node.isModified = False


def main():
    ui = TableManager()
    try:
        ui.open_project(sys.argv[1])
    except IndexError:
        pass
    ui.start()


if __name__ == '__main__':
    main()
