# time series feature construction

# import libraries that will be used throughout the analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("READING IN 2016 TARGETS...")
targets = pd.read_csv("../Input/train_2016_v2.csv")


# label outliers
# (previous inspection of the data reveals that logerrors > 2 and < -2 may be outliers)
logging.debug("LABELLING OUTLIERS...")

length = targets.__len__()
outlier = [0] * length

i = 0
for id, row in targets.iterrows():
    l = row['logerror']

    if l > 2 or l < -2:
        outlier[i] = 1

    i += 1

targets['outlier'] = np.array(outlier)


# add day of the week and month features and holiday flag
logging.debug("ADDING DAY, MONTH, AND HOLIDAY DATA...")

from pandas.tseries.holiday import USFederalHolidayCalendar
import datetime

cal = USFederalHolidayCalendar()
holidays = cal.holidays(start='2016-01-01', end='2016-12-31').to_pydatetime()

weekday = []
month = []
holiday = [0] * length

i = 0
for id, row in targets.iterrows():
    y, m, d = row['transactiondate'].split('-')

    dt = datetime.datetime(int(y), int(m), int(d), 0, 0)
    weekday.append(dt.weekday())
    month.append(int(m))

    if dt in holidays:
        holiday[i] = 1

    i += 1

targets['weekday'] = np.array(weekday)
targets['month'] = np.array(month)
targets['holiday'] = np.array(holiday)

logging.debug(targets)


# merge with property data
logging.debug("READING IN 2016 PROPERTIES...")
properties = pd.read_csv("../Input/properties_2016.csv")

logging.debug("MERGING TWO DATASETS")
combined = pd.merge(targets, properties, on=['parcelid'])

logging.debug(combined.head(3).transpose())


# add weather information
import arrow # learn more: https://python.org/pypi/arrow
from WunderWeather import weather # learn more: https://python.org/pypi/WunderWeather

api_key = ''
extractor = weather.Extract(api_key)

for id, row in combined.iterrows():
    zip = int(row['regionidzip']).__str__()
    date = arrow.get(row['transactiondate'], "YYYY-MM-DD")

    logging.debug("{}, {}, {}".format(zip, date, date.format('YYYMMDD')))

    date_weather = extractor.date(zip, date.format('YYYYMMDD'))

    logging.debug(date_weather)

    break




# add house sales information