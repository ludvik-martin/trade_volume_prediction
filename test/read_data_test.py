import unittest
from util.read_data import DataReader
import numpy as np

class ReadDataTest(unittest.TestCase):

    def setUp(self):
        self.reader = DataReader()

    def test_read_data(self):
        data = self.reader.read_all_data()
        number_of_rows = 4779
        self.assertEqual(len(data), number_of_rows)

    def test_read_data_normalized(self):
        data = self.reader.read_all_data()
        number_of_rows = 4779
        self.assertEqual(len(data), number_of_rows)

    def test_denormalize_data(self):
        df = self.reader.read_all_data()
        df_norm = self.reader.read_all_data_normalized()
        self.assertFalse(np.array_equal(df, df_norm))
        df_denorm = self.reader.denormalize(df_norm)
        not_numeric = ['Month','DayOfWeek']
        self.assertTrue(np.array_equal(df.drop(not_numeric, axis=1).values.round(5), df_denorm.drop(not_numeric, axis=1).round(5).values))
        self.assertTrue(df[not_numeric].equals(df_denorm[not_numeric]))

