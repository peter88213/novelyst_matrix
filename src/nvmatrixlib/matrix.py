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
        colorsFalse = (('white', 'gray95'), ('gray85', 'gray80'))
        colorsTrue = (('blue4', 'red4'), ('blue3', 'red3'))
        row = 0
        bgr = row % 2
        col = 0
        bgc = col % 2
        columns = []
        columns.append(tk.Frame(master))
        columns[col].pack(side=tk.LEFT)
        tk.Label(columns[col], text=' ', bg=colorsFalse[bgr][bgc]).pack(fill=tk.X)
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=novel.scenes[scId].title,
                         bg=colorsFalse[bgr][bgc],
                         justify=tk.LEFT,
                         anchor=tk.W
                         ).pack(fill=tk.X)
        for crId in novel.characters:
            row = 0
            bgr = row % 2
            col += 1
            bgc = col % 2
            columns.append(tk.Frame(master))
            columns[col].pack(side=tk.LEFT)
            tk.Label(columns[col],
                     text=novel.characters[crId].title,
                     bg=colorsFalse[bgr][bgc],
                     justify=tk.LEFT,
                     anchor=tk.W
                     ).pack(fill=tk.X)
            for chId in novel.chapters:
                for scId in novel.chapters[chId].srtScenes:
                    row += 1
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsFalse[bgr][bgc],
                         colorTrue=colorsTrue[bgr][bgc]
                         )
                    node.pack(fill=tk.X)
                    try:
                        if crId in novel.scenes[scId].characters:
                            node.state = True
                    except TypeError:
                        pass


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
