
import logging
import Tkinter as tk

import view
import asset

__all__ = [
    'AppController',
]

class AppController(tk.Tk, object):
    def __init__(self, 
                 name,
                 version,
                 width,
                 height):
        super(AppController, self).__init__()

        self.set_name_and_version(name, version)
        self.set_dimensions(width, height)

        self.asset_controller = asset.AssetController(self)

        self.register_menubar()

    def set_name_and_version(self, name, version):
        logging.debug('Setting app name (%s) and version (%s)' % (name, version))
        self.name = name
        self.version_string = version
        self.version = version.split('.')
        logging.debug('Setting app title')
        self.title(name)

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

        logging.debug('Setting app dimensions (%d x %d)' % (width, height))
        self.geometry('%dx%d' % (width, height))

    def register_menubar(self):
        logging.debug('Setting menubar')
        self.menubar = tk.Menu(self)
        self.register_app_menu()
        self.register_file_menu()
        self.config(menu=self.menubar)

    def register_app_menu(self):
        logging.debug('Registering application menu')
        app_menu = view.AppMenu(self.menubar, name='apple')
        app_menu.set_name_and_version(self.name, self.version_string)
        app_menu.register()

    def register_file_menu(self):
        logging.debug('Registering file menu')
        file_menu = view.FileMenu(self.menubar, tearoff=0)
        file_menu.register(self.asset_controller.add_asset_file_handler)

    def run_forever(self):
        try:
            logging.info('Entering forever loop')
            self.mainloop()
        except KeyboardInterrupt:
            logging.info('User pressed Ctrl-C')
        except Exception:
            logging.error('Exception raised in forever-loop', exc_info=True)