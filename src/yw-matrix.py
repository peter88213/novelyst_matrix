"""A relationship matrix for yw7 files

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import tkinter as tk
from tkinter import messagebox
from pywriter.ui.main_tk import MainTk
from novelyst_matrix import Plugin
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.matrix import Matrix
from nvmatrixlib.node import Node

APPLICATION = 'Relationship Matrix'


class ywMatrix(MainTk):

    def __init__(self):
        kwargs = {
                'root_geometry': '800x500',
                'yw_last_open': '',
                'color_text_bg':'white',
                'color_text_fg':'black',
                }
        super().__init__(APPLICATION, **kwargs)
        self.mainWindow.pack_propagate(0)

    def open_project(self, fileName):
        super().open_project(fileName)
        #--- The Matrix.
        Node.isModified = False
        if self.novel is not None:
            self._matrixWindow = tk.Frame(self.mainWindow)
            self._matrix = Matrix(self._matrixWindow, self.novel)
            self._matrix.set_nodes()
            self._matrixWindow.pack(expand=True)

    def close_project(self, event=None):
        self._apply_changes()
        self._matrix = None
        self._matrixWindow.destroy()
        super().close_project()

    def on_quit(self, event=None):
        self._apply_changes()
        super().on_quit()

    def _apply_changes(self):
        #--- Apply changes.
        if Node.isModified:
            if messagebox.askyesno(PLUGIN, f"{_('Apply changes')}?"):
                self._matrix.get_nodes()
                self.prjFile.write()
            Node.isModified = False


def main():
    ui = ywMatrix()
    try:
        ui.open_project(sys.argv[1])
    except IndexError:
        pass
    ui.start()


if __name__ == '__main__':
    main()
