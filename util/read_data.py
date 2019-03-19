import pandas as pd
import abc
import datetime

class DataReader(abc.ABC):
    def __init__(self):
        super().__init__()

    def read_all_data(self):
        data = pd.read_csv("../data/S&P500.csv")
        data['Date'] = pd.to_datetime(data['Date'])
        data['DayOfWeek'] = data.Date.dt.weekday_name
        return data

#%%

