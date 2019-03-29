import pandas as pd
import abc
import datetime
import numpy as np
from sklearn.preprocessing import StandardScaler

_NOT_NUMERIC_COLS = ['Month','DayOfWeek']
_NOT_NORMALIZED_FEATURES = _NOT_NUMERIC_COLS + ['Volume']


class DataReader(abc.ABC):

    def __init__(self, test_start_date = datetime.datetime(2017, 1, 1)):
        '''

        :param test_start_date: date from which test set starts
        '''
        super().__init__()
        self.test_start_date = test_start_date
        self.label_scaler = StandardScaler()

    def read_all_data(self, file=None):
        '''
        Reads all data from csv file.

        :param file: path to the csv file
        :return: Pandas DataFrame with the data
        '''
        file = "../data/S&P500.csv" if file == None else file
        df = pd.read_csv(file)
        df.Volume = df.Volume.astype(np.float64)
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

    def read_all_data_normalized(self, file=None):
        '''
        Reads all data normalized with StandardScaler.
        :param file:
        :return: normalized data
        '''
        df = self.read_all_data(file)
        normalized = df.copy()
        # do not care about denormalization of features
        feature_scaler = StandardScaler()
        normalized_columns = [item for item in df.columns if item not in _NOT_NORMALIZED_FEATURES]
        normalized[normalized_columns] = feature_scaler.fit_transform(df.drop(_NOT_NORMALIZED_FEATURES, axis=1))
        normalized[['Volume']] = self.label_scaler.fit_transform(df[['Volume']])
        return normalized

    def denormalize_volume(self, df):
        '''
        Denormalizes volume with the same scaler used for normalization.
        :param df:
        :return:
        '''
        denormalized = df.copy()
        denormalized[['Volume']] = self.label_scaler.inverse_transform(df[['Volume']])
        return denormalized

    def read_normalized_data_for_rnn(self, file=None):
        '''
            Creates one-hot features from categorical features: Month, DayOfWeek.
            Removes features that does not seem important from EDA.
        :param file:
        :return:
        '''
        df = self.read_all_data_normalized(file)

        # drop features by EDA
        df = df.drop(['Open', 'High', 'Low', 'Close', 'AdjClose', 'OpenDiff', 'CloseDiff'], axis=1)

        # onge-hot encoding of categorical features
        df = pd.get_dummies(df, columns=['DayOfWeek', 'Month'])
        # float is more efficient than double
        df = df.astype(np.float32)
        df = df.dropna()
        return df

    def prepare_window_features_for_training(self, df, n):
        '''
            Add past window of Volume. HighLowDiff and AdjCloseDiff as new features.
            Creates one-hot features from categorical features: Month, DayOfWeek.
            Also removes features that does not seem important from EDA.

        :param df: original DF
        :param n: length of the window
        :return: df with window features
        '''
        df = df.copy()

        # add past window of Volume and HighLowDiff as new features
        for i in range(1, n + 1):
            df["Volume" + str(i)] = df.Volume.shift(i)
            df["AdjCloseDiff" + str(i)] = df.AdjCloseDiff.shift(i)
            df["HighLowDiff" + str(i)] = df.HighLowDiff.shift(i)

        # one-hot encoding of categorical data
        df = pd.get_dummies(df, columns=['DayOfWeek', 'Month'])

        # drop features by EDA
        df = df.drop(['Open', 'High', 'Low', 'Close', 'AdjClose', 'OpenDiff', 'CloseDiff'], axis=1)

        # we cannot include following features, as we can use historical data from prediction only,
        # not the market data from the same day        df = df.drop(
        df = df.drop(['HighLowDiff', 'AdjCloseDiff'], axis=1)

        return df


    def get_train_data(self, df, train_start_date = datetime.datetime(2000, 1, 1)):
        '''
        :param df:
        :return: tuple (df_train_features, df_train_volume) where df_train_features does not contain label and df_test contains only labels
        '''
        df_train_features = df.drop(['Volume'], axis=1).copy()
        df_train_features = df_train_features[(df_train_features.index < self.test_start_date)
                                              & (df_train_features.index >= train_start_date)]

        df_train_volume = df['Volume']
        df_train_volume = df_train_volume[(df_train_volume.index < self.test_start_date)
                                          & (df_train_volume.index >= train_start_date)]
        return df_train_features, df_train_volume

    def get_test_data(self, df):
        '''
        :param df:
        :return: tuple (df_test_features, df_test_volume) where df_test_features does not contain label and df_test_label contains only labels
        '''
        df_test_features = df.drop(['Volume'], axis=1).copy()
        df_test_features = df_test_features[df_test_features.index >= self.test_start_date]

        df_test_volume = df['Volume']
        df_test_volume = df_test_volume[df_test_volume.index >= self.test_start_date]
        return df_test_features, df_test_volume

