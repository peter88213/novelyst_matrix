"""A standalone application for the nv_matrix plugin.

For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys

from novxlib.novx_globals import _
from novxlib.ui.main_tk import MainTk
from nv_matrix import Plugin
import tkinter as tk

APPLICATION = 'Matrix'


class TableManager(MainTk):

    def __init__(self):
        kwargs = {
                'root_geometry': '800x500',
                'last_open': '',
                'color_text_bg':'white',
                'color_text_fg':'black',
                }
        super().__init__(APPLICATION, **kwargs)

        self.views = []

        # Tools
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label='Tools', menu=self.toolsMenu)
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)

        self.plugin = Plugin()
        self.plugin.install(self)
        self.plugin.enable_menu()

    def refresh_tree(self):
        """Test dummy."""

    def on_quit(self):
        self.plugin.on_quit()
        super().on_quit()


if __name__ == '__main__':
    ui = TableManager()
    ui.open_project(sys.argv[1])
    ui.start()

