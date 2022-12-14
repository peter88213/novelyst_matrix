"""Provide a frame with a vertical scrollbar. 

Based on
https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame"""
import tkinter as tk
from tkinter import ttk


class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a _canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self._canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self._canvas.yview)

        # Reset the view
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # Create a frame inside the _canvas which will be scrolled with it.
        self.interior = ttk.Frame(self._canvas)

        # Track changes to the _canvas and frame width and sync them,
        # also updating the scrollbar.

        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self._canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self._canvas.winfo_width():
                # Update the _canvas's width to fit the inner frame.
                self._canvas.config(width=self.interior.winfo_reqwidth())

        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self._canvas.winfo_width():
                # Update the inner frame's width to fill the _canvas.
                self._canvas.itemconfigure(self._interior_id, width=self._canvas.winfo_width())

        self._canvas.bind('<Configure>', _configure_canvas)

    def create(self):
        self._interior_id = self._canvas.create_window(0, 0, window=self.interior, anchor=tk.NW, tags="self.interior")

