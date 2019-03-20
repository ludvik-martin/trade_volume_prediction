from util.earning_calendar import EarningCalendar
import unittest
import datetime

#%%

class EarningCalendarTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.ec = EarningCalendar()

    def test_earning_events(self):
        date = datetime.datetime(2019, 3, 14)
        expected = (0, 5)
        print(self.ec.earning_events_on(date))
        self.assertEqual(self.ec.earning_events_on(date), expected)


