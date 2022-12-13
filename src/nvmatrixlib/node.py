"""Provide a class representing a visual matrix node.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk


class Node(tk.Label):
    """A visual matrix node, representing a boolean value.
    
    Class variables:
        isModified -- Boolean: True, if at least one instance has changed its state.
    
    Properties:
        state -- Boolean: Node state. Changes its value and color when clicked on.
    """
    isModified = False

    def __init__(self, master, colorFalse='white', colorTrue='black', cnf={}, **kw):
        """Place the node to the master widget.
        
        Optional arguments:
            colorFalse -- str: node color when status is False.
            colorTrue -- str: node color when status is True.
        """
        self.colorTrue = colorTrue
        self.colorFalse = colorFalse
        self._state = False
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
        Node.isModified = True
