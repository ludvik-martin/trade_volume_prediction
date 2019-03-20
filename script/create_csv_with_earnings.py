from util.earning_calendar import EarningCalendar
from util.read_data import  DataReader
import pandas as pd
import datetime
import abc

class SequentalEarnigCalendar(abc.ABC):
    def __init__(self, ec: EarningCalendar):
        super().__init__()
        self.previous_after_market_close = 0
        self.ec = ec

    def earning_events_on(self, date):
        after_market_close, other =  self.ec.earning_events_on(date)
        events = self.previous_after_market_close + other
        self.previous_after_market_close = after_market_close
        return events

def main():
    reader = DataReader()
    df = reader.read_all_data()
    ec = SequentalEarnigCalendar(EarningCalendar())

    years = range(2017, 2019)
    for year in years:
        df_year = df[(df.Date >= datetime.datetime(year, 1, 1)) & (df.Date < datetime.datetime(year + 1, 1, 1))].copy()
        df_year['Earnings'] = df_year.apply(lambda row: ec.earning_events_on(row['Date']), axis=1)
        df_year.to_csv('../data/S&P500_earnings_{}.csv'.format(year))
        print("processed year: {}".format(year))

    df_year_array = [pd.read_csv('../data/S&P500_earnings_{}.csv'.format(year), index_col='Index') for year in years]
    earnings_df = pd.concat(df_year_array, axis=0).sort_index()
    earnings_df.to_csv('../data/S&P500_earnings.csv')
    print("all years processed and stored!")

if __name__ == "__main__":
    main()