import pandas as pd
import dt

import logging
logging.basicConfig(level=logging.DEBUG)

import matplotlib.pyplot as plt

logging.debug("READING IN 2016 TARGETS...")
targets = pd.read_csv("../Input/targets.csv")

# some of the values in the target list appear to be out of order (by date)
# the following code will create a sorted dictionary of dates from which we
# will extract the max, min, and average log error for the data
def getDescriptive(l):
    mx = mn = l[0]
    ave = 0

    for item in l:
        mx = item if item > mx else mx
        mn = item if item < mn else mn
        ave += item

    ave /= float(len(l))

    return mx, mn, ave

date_dict = {}
date_list = []

for id, row in targets.iterrows():
    if id % 1000 == 0:
        logging.debug(id)

    date = row['transactiondate']
    value = row['logerror']

    if date not in date_list:
        date_list.append(date)
        date_dict[date] = [float(value)]
    else:
        date_dict[date].append(float(value))

date_list.sort()

max_series = []
min_series = []
ave_series = []

for date in date_list:
    mx, mn, av = getDescriptive(date_dict[date])

    max_series.append(mx)
    min_series.append(mn)
    ave_series.append(av)

plt.plot(date_list, max_series)
plt.plot(date_list, min_series)
plt.plot(date_list, ave_series)

plt.show()