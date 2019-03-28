import abc
import math
from sklearn.metrics import mean_squared_error, r2_score

class ModelResults(abc.ABC):
    def __init__(self, name, mse, r2, errors, confidence_int_95):
        super().__init__()
        self.name = name
        self.mse = mse
        self.r2 = r2
        self.errors = errors
        self.confidence_int_95 = confidence_int_95

    def __str__(self):
        return "{}: MSE = {:e}, R2 = {:.3f}, confidence interval 95% = ({:,.0f} - {:,.0f})".format(self.name, self.mse, self.r2, self.confidence_int_95[0], self.confidence_int_95[1])


class ModelEvaluator(abc.ABC):
    def __init__(self):
        super().__init__()

    def evaluate(self, model_name, volume_true, volume_pred):
        mse = mean_squared_error(volume_true, volume_pred)
        r2 = r2_score(volume_true, volume_pred)
        errors = volume_pred - volume_true
        sample_mean = errors.mean()
        sigma = math.sqrt((errors ** 2).mean())
        n = errors.size
        # <mean - 1.96 * sigma/sqrt(n), mean + 1.96 * sigma/sqrt(n)>
        confidence_int_95 = [sample_mean - 1.96 * sigma / math.sqrt(n), sample_mean + 1.96 * sigma / math.sqrt(n)]
        return ModelResults(model_name, mse, r2, errors, confidence_int_95)
