import unittest
from util.read_data import DataReader
import numpy as np

class ReadDataTest(unittest.TestCase):

    def setUp(self):
        self.reader = DataReader()

    def test_read_data(self):
        data = self.reader.read_all_data()
        number_of_rows = 4778
        self.assertEqual(len(data), number_of_rows)

    def test_read_data_normalized(self):
        data = self.reader.read_all_data()
        number_of_rows = 4778
        self.assertEqual(len(data), number_of_rows)

    def test_denormalize_data(self):
        df = self.reader.read_all_data()
        df_norm = self.reader.read_all_data_normalized()
        self.assertFalse(np.array_equal(df, df_norm))
        self.assertFalse(np.array_equal(df.drop(['Volume'], axis=1), df_norm.drop(['Volume'], axis=1)))
        df_denorm = self.reader.denormalize_volume(df_norm)
        not_numeric = ['Month','DayOfWeek']
        self.assertTrue(np.array_equal(df['Volume'].round(5), df_denorm['Volume'].round(5).values))
        self.assertTrue(df[not_numeric].equals(df_denorm[not_numeric]))

    def test_get_train_data(self):
        df_norm = self.reader.read_all_data_normalized()
        df_train_features, df_train_label = self.reader.get_train_data(df_norm)
        self.assertFalse('Volume' in df_train_features.columns)
        self.assertEqual(len(df_train_features), 4277)
        self.assertEqual(len(df_train_label), 4277)

    def test_get_test_data(self):
        df_norm = self.reader.read_all_data_normalized()
        df_test_features, df_test_label = self.reader.get_test_data(df_norm)
        self.assertFalse('Volume' in df_test_features.columns)
        self.assertEqual(len(df_test_features), 501)
        self.assertEqual(len(df_test_label), 501)

    def test_prepare_window_features_for_training(self):
        df_norm = self.reader.read_all_data_normalized()
        df_ml = self.reader.prepare_window_features_for_training(df_norm, 1)
