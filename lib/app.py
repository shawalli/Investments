
import Tkinter as tk
from tkFileDialog import askopenfilenames
import time
import atexit

import asset
import canvas
import log

class BasicMenu(object):
    def __init__(self,
                 app_instance,
                 root_menu_instance):
        self._app = app_instance
        self._root_menu = root_menu_instance
        self._log = self._app.get_log()

    def register(self):
        raise NotImplementedError('register() function is not implemented!')

class ApplicationMenu(BasicMenu):
    def _create_about_dialog(self):
        self._log.debug("Creating \"About\' popup")
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
        self._log.debug("Finished creating \"About\' popup")

    def register(self):
        application_menu = tk.Menu(self._root_menu, name='apple')

        about_string = 'About %s' % self._app.name
        application_menu.add_command(label=about_string,
                                     command=self._create_about_dialog)

        self._root_menu.add_cascade(menu=application_menu)

class FileMenu(BasicMenu):
    def _add_asset_files(self):
        self._log.debug("Creating \'Add Asset Files\' file-picker popup")
        asset_filepaths = askopenfilenames(parent=self._app.get_instance_handle())
        self._log.debug("Retrieved asset files")
        self._log.debug(str(asset_filepaths))

        self._log.info("Creating root asset collection")
        self._log.info("Importing asset files")
        coll = asset.AssetCollection(filepath='root')
        for asset_filepath in asset_filepaths:
            self._log.debug("Importing asset file: %s" % asset_filepath)
            #todo: pop-up spreadsheet window to chose row ranges to import
            file_coll = asset.import_asset_file(asset_filepath)
            self._log.debug("Merging imported asset_collection with root")
            coll.update(file_coll)
        self._log.info("Finished importing asset files")

        app_canvas = self._app.get_canvas_handle()
        self._log.debug("Registering root asset_collection with canvas")
        app_canvas.register_data(coll)
        self._log.debug("Drawing canvas")
        self._log.debug("Drawing canvas using root asset_collection data")
        app_canvas.draw_canvas()
        self._log.debug("Finished drawing canvas")

    def register(self):
        file_menu = tk.Menu(self._root_menu, tearoff=0)
        file_menu.add_command(label='Add Asset Files...',
                              command=self._add_asset_files)
        self._root_menu.add_cascade(label='File', menu=file_menu)

class App(object):
    def __init__(self, name, width, height, version):
        self._log = log.initialize_log(name)

        self._log.info("App initialization started at %s" % (time.ctime()))
        self.name = name
        self.version = version

        self._log.debug("Registering log cleanup function with atexit")
        atexit.register(log.finalize_log, self._log)

        self._log.debug("Creating Tk instance")
        self._instance = tk.Tk()

        self._log.debug("Adding app title and adjusting app window size")
        self._instance.title(name)
        self._instance.geometry('%dx%d' % (width, height))

        self._log.debug("Initializing app canvas")
        self._canvas = canvas.Canvas(self, width, height)

        self._log.debug("Registering menubar and menus")
        self.register_menus()

        self._log.info("App initialization complete")

    def run_forever(self):
        try:
            self._log.info("Entering forever-loop")
            self._instance.mainloop()
            self._log.info("Leaving forever-loop")
        except KeyboardInterrupt:
            self._log.info("User pressed ctrl-C")
        except Exception:
            self._log.error("Exception raised in forever-loop", exc_info=True)

    def get_log(self):
        return self._log

    def get_instance_handle(self):
        return self._instance

    def get_canvas_handle(self):
        return self._canvas

    def register_menus(self):
        self._menubar = tk.Menu(self._instance)
        self._menus = list()

        self._log.debug("Registering Application menu")
        menu = ApplicationMenu(self, self._menubar)
        menu.register()
        self._menus.append(menu)

        self._log.debug("Registering File menu")
        menu = FileMenu(self, self._menubar)
        menu.register()
        self._menus.append(menu)

        self._log.debug("Setting menubar in app")
        self._instance.config(menu=self._menubar)