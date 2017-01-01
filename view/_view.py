
import Tkinter as tk
import ttk
# import tkFont
# import logging

from util import classproperty

__all__ = [
    'ViewError',
    'TopLevelView', 'CanvasView',
    'ColorPicker',
]

class ViewError(Exception): pass

class TopLevelView(tk.Toplevel, object):
    def __init__(self,
                 width,
                 height):
        super(TopLevelView, self).__init__()

        self.width = width
        self.height = height
        self.geometry('%dx%d' % (width, height))
        # self.pack()
        # self.place(x=0, y=0, width=width, height=height)

class CanvasView(ttk.Frame, object):
    def __init__(self,
                 master,
                 width,
                 height):
        super(CanvasView, self).__init__(master,
                                   width=width,
                                   height=height)
        self.place(x=0, y=0, width=width, height=height)

        self.master = master
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.place(x=0, y=0, width=width, height=height)

    # @classproperty
    # def title_font(self):
    #     return tkFont.Font(size=20, weight='bold', underline=1)

    @classproperty
    def title_font(self):
        return ('Helvetica', '20', 'bold underline')

class ColorPicker(object):
    EMPTY_COLOR = "#DCDCDC"

    RGB_COLORS = [
        "#4D4D4D", # gray
        "#5DA5DA", # blue
        "#FAA43A", # orange
        "#60BD68", # green
        "#F17CB0", # pink
        "#B2912F", # brown
        "#DECF3F", # yellow
        "#F15854", # red
    ]

    def __init__(self):
        self.index = 0

    def __iter__(self):
        return self

    @classproperty
    def empty_color():
        return ColorPicker.EMPTY_COLOR

    def next(self):
        color = self.RGB_COLORS[self.index]

        self.index += 1

        if self.index >= len(self.RGB_COLORS):
            self.index = 0

        return color