import unittest
from util.read_data import DataReader

class ReadDataTest(unittest.TestCase):

    def setUp(self):
        self.reader = DataReader()

    def test_read_data(self):
        data = self.reader.read_all_data()
        number_of_rows = 4779
        self.assertEqual(len(data), number_of_rows)
