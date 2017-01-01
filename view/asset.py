
import Tkinter as tk
# import ttk
# import tkFont
# import logging

from util import classproperty, math

from _view import CanvasView, ColorPicker

__all__ = [
    'ChartView',
]

class ChartView(CanvasView):
    def __init__(self, master, width, height):
        super(ChartView, self).__init__(master,
                                        width,
                                        height)

        self.data = list()

        self.draw()

    @property
    def chart_location(self):
        x1 = y1 = 20
        x2 = y2 = 0.60 * min(self.width, self.height)

        return (x1, y1, x2, y2)

    @property
    def legend_location(self):
        chart_coords = self.chart_location
        x1 = chart_coords[2] + 60
        y1 = chart_coords[0]
        x2 = x1 + 0.30 * self.width
        y2 = 0.80 * self.height

        return (x1, y1, x2, y2)

    # @classproperty
    # def legend_key_font(self):
    #     return tkFont.Font(size=14)

    @classproperty
    def legend_key_font(self):
        return ('Helvetica', '14')

    def draw(self, data_label='', data=list()):
        self.canvas.delete('all')

        colorized_data = self.draw_chart(data)
        self.draw_legend(data_label, colorized_data)

    def draw_chart(self, data):
        colors = ColorPicker()
        if len(data) == 0:
            self.canvas.create_oval(*self.chart_location,
                                    fill=colors.EMPTY_COLOR)
            colorized_data = None
        else:
            colorized_data = list()
            total = sum([value for name, value in data])
            item_start_deg = 0.00
            for name, value in data:
                item_pct = (value * 100) / total
                item_deg = math.percent_to_degrees(item_pct)
                color = next(colors)

                self.canvas.create_arc(*self.chart_location,
                                       fill=color,
                                       start=item_start_deg,
                                       extent=item_deg)

                colorized_data.append((name, value, item_pct, color))
                item_start_deg += item_deg

        return colorized_data

    def draw_legend(self, data_label, data):
        if (data_label == '') or data is None:
            return

        legend_coords = self.legend_location
        x_ref = legend_coords[0]
        y_ref = legend_coords[1]

        self.canvas.create_text(x_ref,
                                y_ref,
                                font=self.title_font,
                                text=data_label,
                                anchor=tk.NW)
        x_ref += 10
        y_ref += 40

        for name, value, pct, color in data:
            self.canvas.create_rectangle(x_ref, 
                                         y_ref+3,
                                         x_ref+10,
                                         y_ref+13,
                                        fill=color)

            # key name
            self.canvas.create_text(x_ref + 20,
                                    y_ref,
                                    font=self.legend_key_font,
                                    text=name,
                                    anchor=tk.NW)

            # key value
            self.canvas.create_text(x_ref + 60 + 80,
                                    y_ref,
                                    font=self.legend_key_font,
                                    text='$%.2f' % value,
                                    anchor=tk.NE)

            # key percent
            self.canvas.create_text(x_ref + 140 + 80,
                                    y_ref,
                                    font=self.legend_key_font,
                                    text='%.2f%%' % pct,
                                    anchor=tk.NE)

            y_ref += 20