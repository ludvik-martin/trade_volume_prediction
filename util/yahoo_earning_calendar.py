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
        earnings = self.yec.earnings_on(date)
        tickers = set(map(lambda x:x['ticker'], earnings))
        s_and_p_matches = len(tickers.intersection(self.constituents))
        return s_and_p_matches


