"""Provide a class representing a table of relationships.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from pywriter.pywriter_globals import *
from nvmatrixlib.node import Node


class RelationsTable:
    """Represent a table of relationships. 
    
    Public methods:
        set_nodes -- Loop through all nodes, setting states.
        get_nodes -- Loop through all nodes, modifying the scenes according to the states.
    
    The visual part consists of one frame per column, each containing 
    one node per row. 
    The logical part consists of one dictionary per element type (protected instance variables):
    {scene ID: {element Id: node}}
    """

    def __init__(self, master, novel, **kwargs):
        """Draw the matrix with blank nodes.
        
        Positional arguments:
            novel: Novel -- Project reference.
            
        """

        def fill_str(text):
            """Return a string that is at least 7 characters long.
            
            Extend text with spaces so that it does not fall 
            below the length of 7 characters.
            This is for column titles, to widen narrow columns.
            """
            while len(text) < 7:
                text = f' {text} '
            return text

        colorsBackground = ((kwargs['color_bg_00'], kwargs['color_bg_01']),
                            (kwargs['color_bg_10'], kwargs['color_bg_11']))
        self._novel = novel
        columns = []
        col = 0
        bgc = col % 2

        #--- Scene title column.
        tk.Label(master.topLeft, text=_('Scenes')).pack(fill='x')
        tk.Label(master.topLeft, bg=colorsBackground[1][1], text=' ').pack(fill='x')

        #--- Display titles of "normal" scenes.
        row = 0
        self._arcNodes = {}
        self._characterNodes = {}
        self._locationNodes = {}
        self._itemNodes = {}
        self._arcs = []
        for chId in self._novel.srtChapters:
            #--- Find arcs.
            if self._novel.chapters[chId].chType == 2:
                arc = self._novel.chapters[chId].kwVar.get('Field_ArcDefinition', None)
                if arc:
                    if not arc in self._arcs:
                        self._arcs.append(arc)
            elif self._novel.chapters[chId].chType == 0:
                for scId in self._novel.chapters[chId].srtScenes:
                    bgr = row % 2
                    if self._novel.scenes[scId].scType != 0:
                        continue

                    #--- Initialize matrix scene row dictionaries.
                    self._characterNodes[scId] = {}
                    self._locationNodes[scId] = {}
                    self._itemNodes[scId] = {}
                    self._arcNodes[scId] = {}

                    tk.Label(master.rowTitles,
                             text=self._novel.scenes[scId].title,
                             bg=colorsBackground[bgr][1],
                             justify='left',
                             anchor='w'
                             ).pack(fill='x')
                    row += 1
        bgr = row % 2
        tk.Label(master.rowTitles,
                         text=' ',
                         bg=colorsBackground[bgr][1],
                         ).pack(fill='x')
        tk.Label(master.rowTitles,
                         text=_('Scenes'),
                         ).pack(fill='x')

        #--- Arc columns.
        self._scnArcs = {}
        for scId in self._arcNodes:
            self._scnArcs[scId] = string_to_list(self._novel.scenes[scId].scnArcs)
            for arc in self._scnArcs[scId]:
                if not arc in self._arcs:
                    self._arcs.append(arc)
        if self._arcs:
            arcTitleWindow = tk.Frame(master.columnTitles)
            arcTitleWindow.pack(side='left', fill='both')
            tk.Label(arcTitleWindow, text=_('Arcs'), bg=kwargs['color_arc_heading']).pack(fill='x')
            arcTypeColumn = tk.Frame(master.display)
            arcTypeColumn.pack(side='left', fill='both')
            arcColumn = tk.Frame(arcTypeColumn)
            arcColumn.pack(fill='both')
            for arc in self._arcs:
                # Display arc titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                arcTitle = fill_str(arc)
                tk.Label(arcTitleWindow,
                         text=arcTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display arc nodes.
                columns.append(tk.Frame(arcColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._scnArcs:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=kwargs['color_arc_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._arcNodes[scId][arc] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=arcTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(arcTypeColumn, text=_('Arcs'), bg=kwargs['color_arc_heading']).pack(fill='x')

        #--- Character columns.
        if self._novel.characters:
            characterTypeColumn = tk.Frame(master.display)
            characterTypeColumn.pack(side='left', fill='both')
            characterColumn = tk.Frame(characterTypeColumn)
            characterColumn.pack(fill='both')
            characterTitleWindow = tk.Frame(master.columnTitles)
            characterTitleWindow.pack(side='left', fill='both')
            tk.Label(characterTitleWindow, text=_('Characters'), bg=kwargs['color_character_heading']).pack(fill='x')
            for crId in self._novel.srtCharacters:
                # Display character titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                characterTitle = fill_str(self._novel.characters[crId].title)
                tk.Label(characterTitleWindow,
                         text=characterTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display character nodes.
                columns.append(tk.Frame(characterColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._characterNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=kwargs['color_character_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._characterNodes[scId][crId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=characterTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(characterTypeColumn, text=_('Characters'), bg=kwargs['color_character_heading']).pack(fill='x')

        #--- Location columns.
        if self._novel.locations:
            locationTypeColumn = tk.Frame(master.display)
            locationTypeColumn.pack(side='left', fill='both')
            locationColumn = tk.Frame(locationTypeColumn)
            locationColumn.pack(fill='both')
            locationTitleWindow = tk.Frame(master.columnTitles)
            locationTitleWindow.pack(side='left', fill='both')
            tk.Label(locationTitleWindow, text=_('Locations'), bg=kwargs['color_location_heading']).pack(fill='x')
            for lcId in self._novel.srtLocations:
                # Display location titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                locationTitle = fill_str(self._novel.locations[lcId].title)
                tk.Label(locationTitleWindow,
                         text=locationTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display location nodes.
                columns.append(tk.Frame(locationColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._locationNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=kwargs['color_location_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._locationNodes[scId][lcId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=locationTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(locationTypeColumn, text=_('Locations'), bg=kwargs['color_location_heading']).pack(fill='x')

        #--- Item columns.
        if self._novel.items:
            itemTypeColumn = tk.Frame(master.display)
            itemTypeColumn.pack(side='left', fill='both')
            itemColumn = tk.Frame(itemTypeColumn)
            itemColumn.pack(fill='both')
            itemTitleWindow = tk.Frame(master.columnTitles)
            itemTitleWindow.pack(side='left', fill='both')
            tk.Label(itemTitleWindow, text=_('Items'), bg=kwargs['color_item_heading']).pack(fill='x')
            for itId in self._novel.srtItems:
                # Display item titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                itemTitle = fill_str(self._novel.items[itId].title)
                tk.Label(itemTitleWindow,
                         text=itemTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display item nodes.
                columns.append(tk.Frame(itemColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._itemNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=kwargs['color_item_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._itemNodes[scId][itId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=itemTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(itemTypeColumn, text=_('Items'), bg=kwargs['color_item_heading']).pack(fill='x')

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
            scCharacters = []
            for crId in self._novel.characters:
                try:
                    node = self._characterNodes[scId][crId]
                except TypeError:
                    pass
                else:
                    if node.state:
                        scCharacters.append(crId)
            # Create a new scene character list, keeping the old order (POV)
            srtCharacters = []
            for crId in self._novel.scenes[scId].characters:
                if crId in scCharacters:
                    srtCharacters.append(crId)
            for crId in scCharacters:
                if not crId in srtCharacters:
                    srtCharacters.append(crId)
            self._novel.scenes[scId].characters = srtCharacters

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

