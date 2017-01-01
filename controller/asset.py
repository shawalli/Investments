
import logging
from tkFileDialog import askopenfilenames

import model
import view

from _controller import ControllerError

__all__ = [
    'AssetController',
]

class AssetController(object):
    def __init__(self, master):
        logging.info('Initializing asset controller')
        self.master = master

        logging.info('Initializing asset database')
        self.database = model.Database()
        logging.info('Initializing asset class session')
        self.asset_class_session = self.database.new_session()

        logging.info('Initializing chart view')
        self.view = view.ChartView(self.master,
                                   width=self.master.width,
                                   height=self.master.height)
        logging.info('Finished initializing asset controller')

    def add_asset_file_handler(self):
        logging.debug('Creating \'Add Asset Files\' file-picker popup')
        asset_filepaths = askopenfilenames(parent=self.master)
        logging.debug('Retrieved asset files')
        logging.debug(str(asset_filepaths))

        logging.info('Creating root asset collection')
        logging.info('Importing asset files')
        for asset_filepath in asset_filepaths:
            logging.debug('Importing asset file: %s' % asset_filepath)
            #todo: pop-up spreadsheet window to chose row ranges to import
            self.database.load_asset_file(asset_filepath,
                                          self.asset_class_session)
        logging.info('Finished importing asset files')

        logging.info('Rendering updated asset class overview')        
        self.render_asset_class_overview_view()
        logging.info('Finished rendering updated asset class overview')

    def render_asset_class_overview_view(self):
        logging.debug('Rendering asset class overview view')
        data = list()
        logging.info('Querying asset class data')
        for asset_class in self.asset_class_session.query(model.AssetClass).all():
            class_total = 0
            for asset in asset_class.assets:
                class_total += asset.value
            data.append((asset_class.short_name, class_total))

        logging.info('Drawing chart view')
        self.view.draw(data_label='Asset Classes', data=data)