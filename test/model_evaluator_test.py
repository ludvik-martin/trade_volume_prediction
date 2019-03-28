import unittest
from util.evaluator import ModelEvaluator
import pandas as pd

class ModelEvaluatorTest(unittest.TestCase):

    def setUp(self):
        self.evaluator = ModelEvaluator()

    def test_evaluate(self):
        volume_true = pd.Series([374050000, 931800000, 1009000000])
        volume_pred = pd.Series([474050000, 231800000, 809000000])
        results = self.evaluator.evaluate("test model", volume_true, volume_pred)
        print(results)