"""Provide a class representing a matrix of yWriter projects.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from nvmatrixlib.nvmatrix_globals import *


class Matrix:
    """Represent a matrix of relationships. 
    
    """

    def __init__(self, master, novel):
        """Initialize the instance variables.
        
        Positional arguments:
            novel -- Novel: Project reference.
        """
        colorsFalse = (('gray80', 'gray70'), ('white', 'gray90'))
        colorsTrue = (('red3', 'red4'), ('blue3', 'blue4'))
        r = 0
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                tk.Label(master,
                         text=novel.scenes[scId].title,
                         bg=colorsFalse[1][r % 2],
                         justify=tk.LEFT,
                         anchor=tk.W
                         ).grid(sticky='nsew',
                                column=0,
                                row=r)
                for c in range(20):
                    Node(master,
                         colorFalse=colorsFalse[c % 2][r % 2],
                         colorTrue=colorsTrue[c % 2][r % 2]
                         ).grid(column=c + 1, row=r)
                r += 1


class Node(tk.Label):
    """A matrix node, representing a boolean value."""
    SIZE = 1

    def __init__(self, master=None, colorFalse='white', colorTrue='black', cnf={}, **kw):
        self.colorTrue = colorTrue
        self.colorFalse = colorFalse
        self._state = False
        kw['width'] = self.SIZE
        kw['height'] = self.SIZE
        super().__init__(master, cnf, **kw)
        self._set_color()
        self.bind('<Button-1>', self._toggle_state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        self._state = newState
        self._set_color()

    def _set_color(self):
        if self._state:
            self.config(background=self.colorTrue)
        else:
            self.config(background=self.colorFalse)

    def _toggle_state(self, event=None):
        self.state = not self._state
