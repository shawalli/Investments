
import Tkinter as tk
from collections import namedtuple

import util

RGB_COLORS = [
    "#5DA5DA", # blue
    "#FAA43A", # orange
    "#60BD68", # green
    "#F17CB0", # pink
    "#B2912F", # brown
    "#DECF3F", # yellow
    "#F15854", # red
    "#4D4D4D", # gray
]

PieChartItem = namedtuple('PieChartItem', 'name value color')

class Canvas(object):
    def __init__(self, width, height):
        self._data = None
        self._color_index = 0
        self._pie_chart_id = -1
        self._pie_chart_data = list()

        self._instance = tk.Canvas(width=width,
                                   height=height)
        self._instance.pack()

        self._width = width
        self._height = height

    def _get_next_color(self):
        color = RGB_COLORS[self._color_index]
        self._color_index += 1
        if self._color_index >= len(RGB_COLORS):
            self._color_index = 0
        return color

    def register_data(self, asset_collection):
        self._data = asset_collection

    @property
    def pie_chart_coords(self):
        x1 = y1 = 20
        x2 = y2 = 0.60 * min(self._width, self._height)

        return (x1, y1, x2, y2)

    def draw_canvas(self):
        self._instance.delete("all")

        self.draw_pie_chart()


    def draw_pie_chart(self):
        class_totals = self._data.get_asset_class_sums()
        total = self._data.get_total_sum()
        start_offset = 0.00

        for asset_class, value in class_totals.items():
            percent = (value * 100) / total
            degrees = util.percent_to_degrees(percent)
            color = self._get_next_color()
            print('mapping: %s:$%.2f   %.2fpct' % (asset_class, value, percent))
            print('  to %.2fdeg with color:%s' % (degrees, color))

            self._pie_chart_data.append(PieChartItem(asset_class,
                                                     value,
                                                     color))

            self._instance.create_arc(self.pie_chart_coords,
                                      fill=color,
                                      start=start_offset,
                                      extent=degrees)

            start_offset += degrees

# WIDTH = 400
# HEIGHT = 400
# class TestApp(object):
#     def __init__(self, asset_collection):
#         self.app = tk.Tk()
#         self.app.geometry('%dx%d' % (WIDTH, HEIGHT))

#         canvas = Canvas(WIDTH, HEIGHT)

#         canvas.register_data(asset_collection)
#         canvas.draw_canvas()

#         self.app.mainloop()


# # TEST RUN
# import asset

# fname1 = "/Users/katiewallis/Desktop/Shawn/investments_app/InvestmentsApp/sample_values.csv"
# fname2 = "/Users/katiewallis/Desktop/Shawn/investments_app/InvestmentsApp/sample_values2.csv"

# coll1 = asset.import_asset_file(fname1)

# coll2 = asset.import_asset_file(fname2)

# # for k,v in coll1.get_asset_class_sums().items() :
# #     print('%s:$%.2f' % (k,v))

# coll1.update(coll2)

# TestApp(coll1)
