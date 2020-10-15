from dataclasses import dataclass
import pandas as pd
import os
import googlemaps
import json

@dataclass
class FileReader:
    
    context: str = ''
    fname: str = ''
    train: object = None
    test: object = None
    id: str = ''
    label: str = ''

    def new_file(self):
        return os.path.join(self.context, self.fname)

    def csv_to_dframe(self):
        return pd.read_csv(self.new_file(), encoding = 'utf-8', thousands = ',')

    def xls_to_dframe(self, header, usecols):
        return pd.read_excel(self.new_file(),  header=  header, usecols = usecols)

    def create_gmaps(self):
        return googlemaps.Client(key='')
        # AIzaSyBGTLvcXmAfXzJYqNOnU_1-13373A2EFjxiqP41337 1337 
    def json_load(self):
        return json.load(open(self.new_file(), encoding = 'utf-8'))