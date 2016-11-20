
from functools import partial

import Tkinter as tk
from tkFileDialog import askopenfilename

NAME = "Investments"
VERSION="0.1.0"
WIDTH = 400
HEIGHT = 400

def load_csv(app):
    csv_filename = askopenfilename(parent=app)
    # todo: pop up small spreadsheet window to choose spreadsheet ranges

def save_session_to_file():
    pass

def about_dialog():
    toplevel = tk.Toplevel()
    toplevel.geometry('350x100')
    tk.Label(toplevel, text="%s %s" % (NAME, VERSION)).pack()
    tk.Label(toplevel, text="Copyright 2015, Eight Bits Software, LLC").pack()
    tk.Button(toplevel, text="Close", command=toplevel.destroy).pack(pady=10)

def send_diagnostic_data():
    pass

class App(object):
    def __init__(self):
        self.app = tk.Tk()

        # Set app parameters
        self.app.title(NAME)
        self.app.geometry('%dx%d' % (WIDTH, HEIGHT))

        # Set menus
        self.create_menus()

        # Forever loop
        self.app.mainloop()

    def create_menus(self):
        menu = tk.Menu(self.app)

        appmenu = tk.Menu(menu, name='apple')
        appmenu.add_command(label='About ' + NAME, command=about_dialog)
        menu.add_cascade(menu=appmenu)

        filemenu = tk.Menu(menu, tearoff=0)
        filemenu.add_command(label="Add CSV", command=partial(load_csv, self.app))
        filemenu.add_command(label="Save Session", command=save_session_to_file)
        filemenu.add_command(label="Quit", command=self.app.quit)
        menu.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menu, tearoff=0)
        helpmenu.add_command(label="Send Diagnostic Data", command=send_diagnostic_data)
        menu.add_cascade(label="Help", menu=helpmenu)

        self.app.config(menu=menu)

if __name__ == '__main__':
    App()
