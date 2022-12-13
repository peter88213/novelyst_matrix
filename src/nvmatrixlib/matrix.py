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
        colorsCharacter = (('goldenrod1', 'goldenrod3'), ('goldenrod3', 'goldenrod4'))
        colorsLocation = (('coral1', 'coral3'), ('coral3', 'coral4'))
        colorsItem = (('aquamarine1', 'aquamarine3'), ('aquamarine3', 'aquamarine4'))
        colorsArc = (('royalBlue1', 'royalBlue3'), ('royalBlue3', 'royalBlue4'))
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

        #--- Arc columns.
        self._arcNodes = {}
        self._arcs = []
        self._scnArcs = {}
        for chId in novel.chapters:
            for scId in novel.chapters[chId].srtScenes:
                self._arcNodes[scId] = {}
                if novel.scenes[scId].scnArcs:
                    self._scnArcs[scId] = string_to_list(novel.scenes[scId].scnArcs)
                    for arc in self._scnArcs[scId]:
                        if not arc in self._arcs:
                            self._arcs.append(arc)
                else:
                    self._scnArcs[scId] = []
        for arc in self._arcs:
            row = 0
            bgr = row % 2
            col += 1
            bgc = col % 2
            columns.append(tk.Frame(master))
            columns[col].pack(side=tk.LEFT)
            tk.Label(columns[col],
                     text=arc,
                     bg=colorsBackground[bgr][bgc],
                     justify=tk.LEFT,
                     anchor=tk.W
                     ).pack(fill=tk.X)
            for scId in self._scnArcs:
                row += 1
                bgr = row % 2
                node = Node(columns[col],
                     colorFalse=colorsBackground[bgr][bgc],
                     colorTrue=colorsArc[bgr][bgc]
                     )
                node.pack(fill=tk.X)
                self._arcNodes[scId][arc] = node

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
        for scId in self._arcNodes:
            for arc in self._arcs:
                try:
                    self._arcNodes[scId][arc].state = (arc in self._scnArcs[scId])
                except TypeError:
                    pass

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
        for scId in self._arcNodes:
            arcs = []
            for arc in self._arcs:
                try:
                    node = self._arcNodes[scId][arc]
                except TypeError:
                    pass
                else:
                    if node.state:
                        arcs.append(arc)
            self._novel.scenes[scId].scnArcs = list_to_string(arcs)

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


def string_to_list(text, divider=';'):
    """Convert a string into a list with unique elements.
    
    Positional arguments:
        text -- string containing divider-separated substrings.
        
    Optional arguments:
        divider -- string that divides the substrings.
    
    Split a string into a list of strings. Retain the order, but discard duplicates.
    Remove leading and trailing spaces, if any.
    Return a list of strings.
    If an error occurs, return an empty list.
    """
    elements = []
    try:
        tempList = text.split(divider)
        for element in tempList:
            element = element.strip()
            if element and not element in elements:
                elements.append(element)
        return elements

    except:
        return []


def list_to_string(elements, divider=';'):
    """Join strings from a list.
    
    Positional arguments:
        elements -- list of elements to be concatenated.
        
    Optional arguments:
        divider -- string that divides the substrings.
    
    Return a string which is the concatenation of the 
    members of the list of strings "elements", separated by 
    a comma plus a space. The space allows word wrap in 
    spreadsheet cells.
    If an error occurs, return an empty string.
    """
    try:
        text = divider.join(elements)
        return text

    except:
        return ''

