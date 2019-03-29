import seaborn as sns
import pandas as pd
import datetime
from matplotlib import pyplot as plt

def visialize_errors(model_name, true_volume, errors_volume):
    '''
    Visualize graphs of predictons and errors.

    :param model_name:
    :param true_volume: labels
    :param errors_volume: prediction errors
    :return:
    '''
    # reconstruct predictions
    pred_volume = true_volume + errors_volume
    data = pd.DataFrame({'Volume': true_volume, 'Errors':errors_volume, 'Prediction': pred_volume})
    data.index = true_volume.index
    # sample dataset selected based on the the EDA
    # TODO: should be parameter
    data = data.loc[datetime.datetime(2018,1,1):]
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 8)
    plot = sns.lineplot(data=data)
    plot.set_title("Errors for model: {}".format(model_name))
