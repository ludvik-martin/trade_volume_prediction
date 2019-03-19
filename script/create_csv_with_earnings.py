from util.yahoo_earning_calendar import EarningCalendar
from util.read_data import  DataReader
import pandas as pd
import datetime

def main():
    reader = DataReader()
    df = reader.read_all_data()
    ec = EarningCalendar()

    years = range(2008, 2018)
    for year in years:
        df_year = df[(df.Date >= datetime.datetime(year, 1, 1)) & (df.Date < datetime.datetime(year + 1, 1, 1))].copy()
        df_year['Earnings'] = df_year.apply(lambda row: ec.earning_events_on(row['Date']), axis=1)
        df_year.to_csv('../data/S&P500_earnings_{}.csv'.format(year))
        print("processed year: {}".format(year))

    df_year_array = [pd.read_csv('../data/S&P500_earnings_{}.csv'.format(year)) for year in years]
    earnings_df = pd.concat(df_year_array, axis=1, join='inner').sort_index()
    earnings_df.to_csv('../data/S&P500_earnings.csv')
    print("all years processed and stored!")

if __name__ == "__main__":
    main()