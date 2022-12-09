"""A test application for the novelyst_matrix plugin.

For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
from pywriter.ui.main_tk import MainTk
from novelyst_matrix import Plugin

APPLICATION = 'Matrix'


class MatrixTk(MainTk):

    def __init__(self):
        kwargs = {
                'root_geometry': '800x500',
                'yw_last_open': '',
                'color_text_bg':'white',
                'color_text_fg':'black',
                }
        super().__init__(APPLICATION, **kwargs)
        plugin = Plugin()
        plugin.install(self)


if __name__ == '__main__':
    ui = MatrixTk()
    ui.open_project(sys.argv[1])
    ui.start()

