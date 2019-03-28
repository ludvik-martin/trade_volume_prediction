import pandas as pd
import abc
import datetime
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
        normalized = df.copy()
        # do not care about denormalization of features
        feature_scaler = StandardScaler()
        normalized_columns = [item for item in df.columns if item not in _NOT_NORMALIZED_FEATURES]
        normalized[normalized_columns] = feature_scaler.fit_transform(df.drop(_NOT_NORMALIZED_FEATURES, axis=1))
        normalized[['Volume']] = self.label_scaler.fit_transform(df[['Volume']])
        return normalized

    def denormalize_volume(self, df):
        denormalized = df.copy()
        denormalized[['Volume']] = self.label_scaler.inverse_transform(df[['Volume']])
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
        df = df.drop(['HighLowDiff'], axis=1)

        return df


    def get_train_data(self, df):
        '''
        :param df:
        :return: tuple (df_train_features, df_train_label) where df_train_features does not contain label and df_test contains only labels
        '''
        df_train_features = df.drop(['Volume'], axis=1).copy()
        df_train_features = df_train_features[df.index < self.test_start_date]

        df_train_label = df[['Volume']]
        df_train_label = df_train_label[df_train_label.index < self.test_start_date]
        return df_train_features, df_train_label

    def get_test_data(self, df):
        '''
        :param df:
        :return: tuple (df_test_features, df_test_label) where df_test_features does not contain label and df_test_label contains only labels
        '''
        df_test_features = df.drop(['Volume'], axis=1).copy()
        df_test_features = df_test_features[df.index >= self.test_start_date]

        df_test_label = df[['Volume']]
        df_test_label = df_test_label[df_test_label.index >= self.test_start_date]
        return df_test_features, df_test_label

