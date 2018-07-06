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

    if l > 2:
        outlier[i] = 1
    elif l < -2:
        outlier[i] = -1

    i += 1

targets['outlier'] = np.array(outlier)


# add day of the week and month features and holiday flag
logging.debug("ADDING DAY, MONTH, AND HOLIDAY DATA...")

from pandas.tseries.holiday import USFederalHolidayCalendar
import datetime

cal = USFederalHolidayCalendar()
holidays = cal.holidays(start='2016-01-01', end='2016-12-31').to_pydatetime()

mon = [0] * length
tue = [0] * length
wed = [0] * length
thu = [0] * length
fri = [0] * length
sat = [0] * length
sun = [0] * length
weekday = [mon, tue, wed, thu, fri, sat, sun]
weekday_name = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

jan = [0] * length
feb = [0] * length
mar = [0] * length
apr = [0] * length
may = [0] * length
jun = [0] * length
jul = [0] * length
aug = [0] * length
sep = [0] * length
oct = [0] * length
nov = [0] * length
dec = [0] * length
month = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
month_name = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

holiday = [0] * length

i = 0
for id, row in targets.iterrows():
    y, m, d = row['transactiondate'].split('-')

    dt = datetime.datetime(int(y), int(m), int(d), 0, 0)

    weekday[dt.weekday()][i] = 1
    month[int(m)-1][i] = 1

    if dt in holidays:
        holiday[i] = 1

    i += 1

i = 0
for name in weekday_name:
    targets[name] = np.array(weekday[i])
    i += 1

i = 0
for name in month_name:
    targets[name] = np.array(month[i])
    i += 1

targets['holiday'] = np.array(holiday)

logging.debug(targets)


# merge with property data
logging.debug("READING IN 2016 PROPERTIES...")
properties = pd.read_csv("../Input/properties_2016.csv")

logging.debug("MERGING TWO DATASETS")
combined = pd.merge(targets, properties, on=['parcelid'])

logging.debug(combined.head(3).transpose())


# add weather information
logging.debug("READING IN WEATHER DATA...")
weather = pd.read_csv("../Input/weather.csv")

delete = ["STATION","NAME","LATITUDE","LONGITUDE","ELEVATION","AWND_ATTRIBUTES","PGTM","PGTM_ATTRIBUTES",
          "PRCP_ATTRIBUTES","SNOW_ATTRIBUTES","SNWD_ATTRIBUTES","TAVG_ATTRIBUTES","TMAX_ATTRIBUTES","TMIN_ATTRIBUTES",
          "WDF2","WDF2_ATTRIBUTES","WDF5","WDF5_ATTRIBUTES","WSF2","WSF2_ATTRIBUTES","WSF5","WSF5_ATTRIBUTES",
          "WT01_ATTRIBUTES","WT02_ATTRIBUTES","WT03_ATTRIBUTES","WT08_ATTRIBUTES"]

weather.drop(delete, axis=1, inplace=True)

combined = pd.merge(combined, weather, left_on=['transactiondate'], right_on=['DATE'])
# combined.drop(['DATE'])

logging.debug("WRITING OUT COMBINED DATA...")
combined.to_csv("../Input/combined_2016.csv", sep=',', encoding='utf-8')
logging.debug(combined.head(3).transpose())
logging.debug(combined.tail(3).transpose())

# add house sales information



# look at correlations
logging.debug("CALCULATING CORRELATIONS...")
c = combined.corr()
logging.debug(c)