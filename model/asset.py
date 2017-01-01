
import logging
import csv
from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, Float, ForeignKey, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from util import money
from _model import ModelError

TableBaseClass = declarative_base()
SessionFactory = sessionmaker()

__all__ = [
    'AssetClass', 'Asset', 'Database',
]

class AssetClass(TableBaseClass):
    __tablename__ = 'asset_classes'

    id = Column(Integer, primary_key=True)
    short_name = Column('short_name', String(8))

    def __str__(self):
        return str(self.short_name)

    def __repr__(self):
        return '<AssetClass(short_name=%s)>' % self.short_name

class Asset(TableBaseClass):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(16))
    quantity = Column('quantity', Float)
    price = Column('price', Float)
    value = Column('value', Float)
    asset_class_id = Column(Integer, ForeignKey('asset_classes.id'))

    def __repr__(self):
        return '<Asset(name=%s quantity=%.2f price=$%.2f value=$%.2f asset_class=%s)>' % (
            self.name, self.quantity, self.price, self.value, str(self.asset_class))

class Database(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        # self.engine = create_engine('sqlite:///dev.db', echo=False)
        SessionFactory.configure(bind=self.engine)
        TableBaseClass.metadata.create_all(self.engine)

    @staticmethod
    def new_session():
        return SessionFactory()

    @staticmethod
    def get_asset_class(session, short_name, create_if_nonexist=True):
        match = session.query(AssetClass).filter_by(short_name=short_name)

        if match.count() > 1:
            raise ModelError(('Asset class short name \'%s\' too ambiguous '
                              '(multiple asset classes matched)' % short_name))
        elif match.count() == 1:
            if create_if_nonexist is True:
                asset_class = match[0]
            else:
                raise ModelError('Asset class short name \'%s\' does not exist' % short_name)
        else:
            asset_class = AssetClass(short_name=short_name)
            session.add(asset_class)
        return asset_class

    @staticmethod
    def load_asset_file(filepath, session):
        logging.info('Loading asset file: %s' % filepath)
        with open(filepath, 'rU') as ifile:
            ireader = csv.reader(ifile,
                                 delimiter=',',
                                 dialect=csv.excel_tab)

            for row in ireader:
                (name,
                 description,
                 quantity,
                 price,
                 day_price,
                 value,
                 day_value,
                 day_change,
                 asset_class_name) = row

                name = name.strip()
                quantity = money.financial_string_to_float(quantity)
                price = money.financial_string_to_float(price)
                value = money.financial_string_to_float(value)
                asset_class_name = asset_class_name.strip().upper()

                asset_class = Database.get_asset_class(session, asset_class_name)

                asset = Asset(name=name,
                              quantity=quantity,
                              price=price,
                              value=value)
                asset_class.assets.append(asset)

        session.commit()

        return session

# Set up table relationships
AssetClass.assets = relationship('Asset', order_by=Asset.id, back_populates='asset_class')
Asset.asset_class = relationship('AssetClass', back_populates='assets')