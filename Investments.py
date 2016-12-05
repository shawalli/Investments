
import lib.app as app

NAME = "Investments"
VERSION="0.1.0"
WIDTH = 400
HEIGHT = 400

root = app.App(NAME, WIDTH, HEIGHT, VERSION)
root.run_forever()