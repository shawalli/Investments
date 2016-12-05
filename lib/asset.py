import csv
from collections import OrderedDict
import hashlib

import util

class AssetCollection(OrderedDict):
    def __init__(self, filepath):
        self._hash = util.generate_hash_id(filepath)

        super(AssetCollection, self).__init__()

    def __str__(self):
        s = ['< AssetCollection >']

        for asset_class in self.asset_classes:
            s.append('  Class: %s' % (asset_class))
            for asset in self[asset_class]:
                s.append('    ' + str(asset))
        return '\n'.join(s)

    @property
    def asset_classes(self):
        return self.keys()

    def add_asset(self, asset, asset_class):
        if asset_class not in self.asset_classes:
            self[asset_class] = list()

        found_asset = self.find_asset(asset.name, asset_class)
        if found_asset is None:
            self[asset_class].append(asset)
        else:
            found_asset.update(asset)

    def find_asset(self, name, asset_class):
        assets = self.get(asset_class, list())
        for asset in assets:
            if asset.name == name:
                return asset
        return None

    def get_asset_class_sums(self):
        totals = dict()
        for asset_class in self.asset_classes:
            totals[asset_class] = 0.00
            for asset in self[asset_class]:
                totals[asset_class] += asset.value
        return totals

    def get_total_sum(self):
        total = 0.00
        for asset_class in self.asset_classes:
            for asset in self[asset_class]:
                total += asset.value
        return total

    def update(self, other):
        for other_asset_class in other.asset_classes:
            for other_asset in other[other_asset_class]:
                self.add_asset(other_asset, other_asset_class)

class Asset(object):
    def __init__(self,
                 name,
                 asset_class,
                 value,
                 description=''):
        self.name = name
        self.asset_class = asset_class
        self.value = value
        self.description = description

    def __str__(self):
        return ("< Asset:%s cls:%s val:$%.2f >" %
                (self.name, self.asset_class, self.value))

    def update(self, other):
        if ((other.name == self.name) and
            (other.asset_class == self.asset_class)):
            self.value += other.value

def import_asset_file(filepath):
    coll = AssetCollection(filepath)

    with open(filepath, 'rU') as i_file:
        i_reader = csv.reader(i_file,
                              delimiter=',',
                              dialect=csv.excel_tab)

        for row in i_reader:
            (name,
             description,
             quantity,
             price,
             day_price,
             value,
             day_value,
             day_change,
             asset_class) = row

            name = name.strip()
            description = description.strip()
            asset_class = asset_class.strip()

            value = util.financial_string_to_float(value)

            asset = Asset(name,
                          asset_class,
                          value,
                          description)

            coll.add_asset(asset, asset_class)
    return coll






