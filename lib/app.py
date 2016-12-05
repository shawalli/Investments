
import Tkinter as tk
from tkFileDialog import askopenfilenames

import asset
import canvas

class BasicMenu(object):
    def __init__(self,
                 app_instance,
                 root_menu_instance):
        self._app = app_instance
        self._root_menu = root_menu_instance

    def register(self):
        raise NotImplementedError('register() function is not implemented!')

class ApplicationMenu(BasicMenu):
    def _create_about_dialog(self):
        top_level = tk.Toplevel()
        top_level.geometry('350x100')

        version_string = '%s %s' % (self._app.name, self._app.version)
        version_label = tk.Label(top_level, text=version_string)
        version_label.pack()

        copyright_string = 'Copyright 2017, Eight Bits Software, LLC'
        copyright_label = tk.Label(top_level, text=copyright_string)
        copyright_label.pack()

        close_button = tk.Button(top_level,
                                 text='Close',
                                 command=top_level.destroy)
        close_button.pack(pady=10)

    def register(self):
        application_menu = tk.Menu(self._root_menu, name='apple')

        about_string = 'About %s' % self._app.name
        application_menu.add_command(label=about_string,
                                     command=self._create_about_dialog)

        self._root_menu.add_cascade(menu=application_menu)

class FileMenu(BasicMenu):
    def _add_asset_files(self):
        asset_filepaths = askopenfilenames(parent=self._app.get_instance_handle())

        coll = asset.AssetCollection(filepath='root')
        for asset_filepath in asset_filepaths:
            #todo: pop-up spreadsheet window to chose row ranges to import
            file_coll = asset.import_asset_file(asset_filepath)
            coll.update(file_coll)

        app_canvas = self._app.get_canvas_handle()
        app_canvas.register_data(coll)
        app_canvas.draw_canvas()

    def register(self):
        file_menu = tk.Menu(self._root_menu, tearoff=0)
        file_menu.add_command(label='Add Asset Files...',
                              command=self._add_asset_files)
        self._root_menu.add_cascade(label='File', menu=file_menu)

class App(object):
    def __init__(self, name, width, height, version):
        self.name = name
        self.version = version

        self._instance = tk.Tk()

        self._instance.title(name)
        self._instance.geometry('%dx%d' % (width, height))

        self._canvas = canvas.Canvas(width, height)

        self.register_menus()

    def run_forever(self):
        self._instance.mainloop()

    def get_instance_handle(self):
        return self._instance

    def get_canvas_handle(self):
        return self._canvas

    def register_menus(self):
        self._menubar = tk.Menu(self._instance)
        self._menus = list()

        menu = ApplicationMenu(self, self._menubar)
        menu.register()
        self._menus.append(menu)

        menu = FileMenu(self, self._menubar)
        menu.register()
        self._menus.append(menu)

        self._instance.config(menu=self._menubar)





