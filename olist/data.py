import os
import pandas as pd

# class that pulls csv files from raw_data folder

class Olist():
    def get_data(self):

        csv_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'raw_data'))
        file_names = [n for n in os.listdir(csv_path) if n[:-4]== '.csv']
        key_names = [n.strip('dataset.csv').strip('olist').strip('_') for n in os.listdir(csv_path)]
        data_list = [pd.read_csv(os.path.join(csv_path, n)) for n in file_names]
        data_dict = dict(zip(key_names, data_list))

        return data_dict


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")

print(Olist().get_data())
