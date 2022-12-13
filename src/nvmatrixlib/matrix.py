"""Provide a class representing a matrix of yWriter projects.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from nvmatrixlib.nvmatrix_globals import *
from nvmatrixlib.node import Node


class Matrix:
    """Represent a matrix of relationships. 
    
    Public methods:
        set_nodes -- Loop through all nodes, setting states.
        get_nodes -- Loop through all nodes, modifying the scenes according to the states.
    
    The visual part consists of one frame per column, each containing 
    one node per row. 
    The logical part consists of one dictionary per element type (protected instance variables):
    {scene ID: {element Id: node}}
    """

    def __init__(self, master, novel):
        """Draw the matrix with blank nodes.
        
        Positional arguments:
            novel -- Novel: Project reference.
            
        """
        self._novel = novel
        colorsBackground = (('white', 'gray95'), ('gray85', 'gray80'))
        colorsCharacter = (('goldenrod3', 'orange3'), ('goldenrod4', 'orange4'))
        colorsLocation = (('brown3', 'red3'), ('brown4', 'red4'))
        colorsItem = (('green3', 'blue3'), ('green4', 'blue4'))
        row = 0
        bgr = row % 2
        col = 0
        bgc = col % 2
        columns = []
        columns.append(tk.Frame(master))
        columns[col].pack(side=tk.LEFT)
        tk.Label(columns[col], text=' ', bg=colorsBackground[bgr][bgc]).pack(fill=tk.X)

        #--- Scene title column.
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=novel.scenes[scId].title,
                         bg=colorsBackground[bgr][bgc],
                         justify=tk.LEFT,
                         anchor=tk.W
                         ).pack(fill=tk.X)

        #--- Character columns.
        self._characterNodes = {}
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                self._characterNodes[scId] = {}
        for crId in novel.characters:
            row = 0
            bgr = row % 2
            col += 1
            bgc = col % 2
            columns.append(tk.Frame(master))
            columns[col].pack(side=tk.LEFT)
            tk.Label(columns[col],
                     text=novel.characters[crId].title,
                     bg=colorsBackground[bgr][bgc],
                     justify=tk.LEFT,
                     anchor=tk.W
                     ).pack(fill=tk.X)
            for chId in novel.chapters:
                for scId in novel.chapters[chId].srtScenes:
                    row += 1
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=colorsCharacter[bgr][bgc]
                         )
                    node.pack(fill=tk.X)
                    self._characterNodes[scId][crId] = node

        #--- Location columns.
        self._locationNodes = {}
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                self._locationNodes[scId] = {}
        for lcId in novel.locations:
            row = 0
            bgr = row % 2
            col += 1
            bgc = col % 2
            columns.append(tk.Frame(master))
            columns[col].pack(side=tk.LEFT)
            tk.Label(columns[col],
                     text=novel.locations[lcId].title,
                     bg=colorsBackground[bgr][bgc],
                     justify=tk.LEFT,
                     anchor=tk.W
                     ).pack(fill=tk.X)
            for chId in novel.chapters:
                for scId in novel.chapters[chId].srtScenes:
                    row += 1
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=colorsLocation[bgr][bgc]
                         )
                    node.pack(fill=tk.X)
                    self._locationNodes[scId][lcId] = node

        #--- Item columns.
        self._itemNodes = {}
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                self._itemNodes[scId] = {}
        for itId in novel.items:
            row = 0
            bgr = row % 2
            col += 1
            bgc = col % 2
            columns.append(tk.Frame(master))
            columns[col].pack(side=tk.LEFT)
            tk.Label(columns[col],
                     text=novel.items[itId].title,
                     bg=colorsBackground[bgr][bgc],
                     justify=tk.LEFT,
                     anchor=tk.W
                     ).pack(fill=tk.X)
            for chId in novel.chapters:
                for scId in novel.chapters[chId].srtScenes:
                    row += 1
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=colorsItem[bgr][bgc]
                         )
                    node.pack(fill=tk.X)
                    self._itemNodes[scId][itId] = node

    def set_nodes(self):
        """Loop through all nodes, setting states."""
        for scId in self._characterNodes:
            for crId in self._novel.characters:
                try:
                    self._characterNodes[scId][crId].state = (crId in self._novel.scenes[scId].characters)
                except TypeError:
                    pass

        for scId in self._locationNodes:
            for lcId in self._novel.locations:
                try:
                    self._locationNodes[scId][lcId].state = (lcId in self._novel.scenes[scId].locations)
                except TypeError:
                    pass

        for scId in self._itemNodes:
            for itId in self._novel.items:
                try:
                    self._itemNodes[scId][itId].state = (itId in self._novel.scenes[scId].items)
                except TypeError:
                    pass

    def get_nodes(self):
        """Loop through all nodes, modifying the scenes according to the states."""
        for scId in self._characterNodes:
            self._novel.scenes[scId].characters = []
            for crId in self._novel.characters:
                try:
                    node = self._characterNodes[scId][crId]
                except TypeError:
                    pass
                else:
                    if node.state:
                        self._novel.scenes[scId].characters.append(crId)

        for scId in self._locationNodes:
            self._novel.scenes[scId].locations = []
            for lcId in self._novel.locations:
                try:
                    node = self._locationNodes[scId][lcId]
                except TypeError:
                    pass
                else:
                    if node.state:
                        self._novel.scenes[scId].locations.append(lcId)

        for scId in self._itemNodes:
            self._novel.scenes[scId].items = []
            for itId in self._novel.items:
                try:
                    node = self._itemNodes[scId][itId]
                except TypeError:
                    pass
                else:
                    if node.state:
                        self._novel.scenes[scId].items.append(itId)

