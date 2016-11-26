
from functools import partial
import csv
import string

import Tkinter as tk
from tkFileDialog import askopenfilenames

#import lib.logging as logging

NAME = "Investments"
VERSION="0.1.0"
WIDTH = 400
HEIGHT = 400

## logging
#logging.basicConfig(format=LOGGING.LOG_FORMAT)
#logger = logging.getLogger('logger')
#logger.setLevel(logging.DEBUG)

#consoleHandler = logging.StreamHandler(sys.stdout)
#consoleHandler.setLevel(logging.DEBUG)
#consoleHandler.setFormatter(formatter)

#fileHandler = logging.FileHandler('tmp_log2.log', delay=True)
#fileHandler.setLevel(logging.DEBUG)
#fileHandler.setFormatter(formatter)

#memoryHandler = MyMemoryHandler(1024*10, logging.DEBUG, fileHandler)
#memoryHandler.setFormatter(formatter)

#logger.addHandler(memoryHandler)

# test
#logger.info('TEST')

class InvestmentClassDict(dict):
    def __str__(self):
        s = list()
        for k,v in self.items():
            s += ['%s: %s' % (k, str(v))]
        return '\n'.join(s)

    def update(self, other):
        for other_key in other.keys():
            if self.has_key(other_key) is False:
                self[other_key] = other[other_key]
            else:
                self[other_key].update(other[other_key])

class Share(object):
    def __init__(self,
                 name,
                 investment_class,
                 description='',
                 quantity=0.00,
                 price=0.00,
                 value=0.00):
        self.name = name
        self.investment_class = investment_class
        self.description = description
        self.records = [(quantity, price, value)]

    def __str__(self):
        value = 0.00
        quantity = 0.00
        for record in self.records:
            value += record[2]
            quantity += record[0]
        return "q:%d  v:%.2f" % (quantity, value)

    def update(self, other):
        if other.name != self.name:
            raise Exception('Investment names do not match! %s != %s' % (self.name, other.name))

        self.records.extend(other.records) 

def string_to_float(s):
    print(s)
    neg_trans = string.maketrans('(','-')
    return float(s.translate(neg_trans, '$,)'))

def process_csv(filepath):
    investments = dict()
    with open(filepath, 'rU') as f:
        f_reader = csv.reader(f, delimiter=',', dialect=csv.excel_tab)
        for row in f_reader:
            (name,
             description,
             quantity,
             price,
             day_price,
             value,
             day_value,
             day_change,
             investment_class) = row

            price = string_to_float(price)
            value = string_to_float(value)
            quantity = string_to_float(quantity)

            entry = Share(name,
                          investment_class,
                          description,
                          quantity,
                          price,
                          value)

            if investment_class not in investments.keys():
                investments[investment_class] = InvestmentClassDict()

            investments[investment_class][name] = entry

    return investments

def process_csvs(app):
    csv_filepaths = askopenfilenames(parent=app)
    # todo: pop up small spreadsheet window to choose spreadsheet ranges

    investments = InvestmentClassDict()
    for csv_filepath in csv_filepaths:
        cur_investments = process_csv(csv_filepath)
        for k,v in cur_investments.items():
            if investments.has_key(k) is False:
                investments[k] = v
            else:
                investments[k].update(v)
    for k,v in investments.items():
        print("%s:" % k)
        for line in str(v).splitlines():
            print('  ' + line)

    investment_totals = dict()
    total_value = 0.00
    for investment_class in investments.keys():
        investment_totals[investment_class] = 0.00
        for share_name in investments[investment_class].keys():
            for record in investments[investment_class][share_name].records:
                investment_totals[investment_class] += record[2]
        total_value += investment_totals[investment_class]
    print('Total value:$%.2f' % (total_value,))
    print(investment_totals)

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
        filemenu.add_command(label="Add CSV", command=partial(process_csvs, self.app))
        filemenu.add_command(label="Save Session", command=save_session_to_file)
        filemenu.add_command(label="Quit", command=self.app.quit)
        menu.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menu, tearoff=0)
        helpmenu.add_command(label="Send Diagnostic Data", command=send_diagnostic_data)
        menu.add_cascade(label="Help", menu=helpmenu)

        self.app.config(menu=menu)

if __name__ == '__main__':
    try:
        App()
    except KeyboardInterrupt:
        print('User terminated application')
