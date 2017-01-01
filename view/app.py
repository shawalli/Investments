
import logging
import Tkinter as tk

from _view import TopLevelView
import model

__all__ = [
    'Menu', 'AppMenu', 'FileMenu',
]

class Menu(tk.Menu):
    def register(self):
        raise NotImplementedError()

class AppMenu(tk.Menu):
    def set_name_and_version(self, name, version):
        self.name = name
        self.version = version

    def render_about_frame(self):
        logging.debug('Creating \'About\' frame')

        about_frame = TopLevelView(350, 100)

        version_text = '%s %s' % (self.name, self.version)
        version_label = tk.Label(about_frame,
                                 # anchor=tk.N,
                                 text=version_text)
        version_label.pack()

        copyright_text = 'Copyright 2017, Eight Bits Software, LLC'
        copyright_label = tk.Label(about_frame,
                                   # anchor=tk.N,
                                   text=copyright_text)
        copyright_label.pack()

        close_button = tk.Button(about_frame,
                                 text='Close',
                                 command=about_frame.destroy)
        close_button.pack()
        logging.debug('Finished creating \'About\' frame')

    def register(self):
        about_button_text = 'About %s' % self.name
        self.add_command(label=about_button_text,
                             command=self.render_about_frame)
        self.master.add_cascade(menu=self)

class FileMenu(Menu):
    def register(self, view_handler):
        self.add_command(label='Add Asset Files...',
                         command=view_handler)
        self.master.add_cascade(label='File', menu=self)






