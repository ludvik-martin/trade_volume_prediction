import abc
from sklearn.metrics import mean_squared_error

class ModelEvaluator(abc.ABC):
    def __init__(self):
        super().__self__()

    def mse(self, df):
        y_pred = df.Volume.rolling(n).mean().shift(1)
        y_test_pred
        mse = mean_squared_error(y_test_true, y_test_pred)
        r2 = r2_score(y_test_true, y_test_pred)

