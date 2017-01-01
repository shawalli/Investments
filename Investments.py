
import controller
import util.logger

NAME = 'Investments'
VERSION='0.1.0'
WIDTH = 600
HEIGHT = 400

util.logger.initialize_log(NAME)
# util.logger.write_log_to_file()

app_controller = controller.AppController(NAME, 
                                          VERSION,
                                          WIDTH,
                                          HEIGHT)
app_controller.run_forever()

util.logger.write_log_to_file()