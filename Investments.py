import Tkinter as tk

NAME = "Investments"
WIDTH = 400
HEIGHT = 400

class App(object):
    def __init__(self):
        self.app = tk.Tk()
        self.app.title(NAME)
        self.app.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.app.mainloop()

if __name__ == '__main__':
    App()
