import pandas as pd
import abc
import datetime
from sklearn.preprocessing import StandardScaler

_NOT_NUMERIC_COLS = ['Month','DayOfWeek']

class DataReader(abc.ABC):
    def __init__(self):
        super().__init__()
        self.scaler = StandardScaler()

    def read_all_data(self):
        df = pd.read_csv("../data/S&P500.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df['DayOfWeek'] = df.Date.dt.weekday_name
        df['Month'] = df.Date.dt.month
        df['AdjClose'] = df['Adj Close']
        # Daily changes
        df['OpenDiff'] = df['Open'] - df['Open'].shift(1)
        df['CloseDiff'] = df['Close'] - df['Close'].shift(1)
        df['AdjCloseDiff'] = df['AdjClose'] - df['AdjClose'].shift(1)
        df['HighLowDiff'] = df['High'] - df['Low']
        df.index = df.Date
        # remove duplicite field
        df = df.drop(['Date', 'Adj Close'], axis=1)
        df = df.dropna()
        return df

    def read_all_data_normalized(self):
        df = self.read_all_data()
        df = df.copy()
        normalized_columns = [item for item in df.columns if item not in _NOT_NUMERIC_COLS]
        numeric_normalized_df = self.scaler.fit_transform(df.drop(_NOT_NUMERIC_COLS, axis=1))
        normalized = pd.DataFrame(numeric_normalized_df, columns=normalized_columns)
        normalized.index = df.index
        normalized[_NOT_NUMERIC_COLS] = df[_NOT_NUMERIC_COLS]
        return normalized

    def denormalize(self, df):
        df = df.copy()
        normalized_columns = [item for item in df.columns if item not in _NOT_NUMERIC_COLS]
        numeric_denormaliezd_df = self.scaler.inverse_transform(df.drop(_NOT_NUMERIC_COLS, axis=1))
        denormalized = pd.DataFrame(numeric_denormaliezd_df, columns=normalized_columns)
        denormalized.index = df.index
        denormalized[_NOT_NUMERIC_COLS] = df[_NOT_NUMERIC_COLS]
        return denormalized


    def prepare_window_features_for_training(self, df, n):
        '''
            Add past window of Volume and HighLowDiff as new features. Also removes features that does not seem
            important from EDA.

        :param df: original DF
        :param n: length of the window
        :return: df with window features
        '''
        df = df.copy()

        # add past window of Volume and HighLowDiff as new features
        for i in range(1, n + 1):
            df["Volume" + str(i)] = df.Volume.shift(i)
            df["AdjCloseDiff" + str(i)] = df.AdjCloseDiff.shift(i)

        # one-hot encoding of categorical data
        df = pd.get_dummies(df, columns=['DayOfWeek', 'Month'])

        # drop features by EDA
        df = df.drop(['Open', 'High', 'Low', 'Close', 'AdjClose', 'OpenDiff', 'CloseDiff', 'AdjCloseDiff'], axis=1)

        # we cannot include following features, as we can use historical data from prediction only,
        # not the market data from the same day        df = df.drop(
        df = df.drop(['Volume', 'HighLowDiff'], axis=1)

        # drop NaN values
        df = df.dropna()
        return df

#%%


