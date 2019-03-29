import unittest
from util.evaluator import ModelEvaluator
import pandas as pd
from sklearn.preprocessing import StandardScaler

class ModelEvaluatorTest(unittest.TestCase):

    def test_evaluate(self):
        evaluator = ModelEvaluator()
        volume_true = pd.Series([374050000, 931800000, 1009000000])
        volume_pred = pd.Series([474050000, 231800000, 809000000])
        results = evaluator.evaluate("test model", volume_true, volume_pred)

    def test_evaluate_with_scaler(self):
        scaler = StandardScaler()
        evaluator = ModelEvaluator(scaler)
        volume_true = pd.Series([374050000., 931800000., 1009000000.])
        volume_true = scaler.fit_transform(pd.DataFrame({'Volume': volume_true}))
        volume_true = pd.Series(volume_true[:,0])
        volume_pred = pd.Series([474050000., 231800000., 809000000.])
        volume_pred = scaler.transform(pd.DataFrame({'Volume':volume_pred}))
        volume_pred = pd.Series(volume_pred[:,0])
        results = evaluator.evaluate("test model", volume_true, volume_pred)
