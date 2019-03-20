import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pandas as pd
import abc

#%%

class EarningCalendar(abc.ABC):
    def __init__(self):
        super().__init__()
        self.yec = YahooEarningsCalendar()
        constituents_df = pd.read_csv("../data/constituents.csv")
        self.constituents = set(constituents_df.Symbol.values)

    def earning_events_on(self, date):
        '''

        :param date: date of interest
        :return: tuple (number of earnings reported after the market closes, number of all other earning events)
        '''
        earnings = self.yec.earnings_on(date)
        # filter only S&P tickers
        earnings = list(filter(lambda x: x['ticker'] in self.constituents, earnings))
        # after market close earnings - will be added to the next market day
        after_market_close = len(list(filter(lambda x: x['startdatetimetype'] == 'AMC', earnings)))
        others = len(earnings) - after_market_close

        s_and_p_matches = (after_market_close, others)
        return s_and_p_matches


