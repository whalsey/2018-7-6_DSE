# import libraries that will be used throughout the analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("READING IN WEATHER DATA...")
weather = pd.read_csv("../Input/weather.csv")

delete = ["STATION","NAME","LATITUDE","LONGITUDE","ELEVATION","AWND_ATTRIBUTES","PGTM","PGTM_ATTRIBUTES",
          "PRCP_ATTRIBUTES","SNOW_ATTRIBUTES","SNWD_ATTRIBUTES","TAVG_ATTRIBUTES","TMAX_ATTRIBUTES","TMIN_ATTRIBUTES",
          "WDF2","WDF2_ATTRIBUTES","WDF5","WDF5_ATTRIBUTES","WSF2","WSF2_ATTRIBUTES","WSF5","WSF5_ATTRIBUTES",
          "WT01_ATTRIBUTES","WT02_ATTRIBUTES","WT03_ATTRIBUTES","WT08_ATTRIBUTES"]

weather.drop(delete, axis=1, inplace=True)

logging.debug(weather.head(3).transpose())
logging.debug(weather.tail(3).transpose())

# AWND
# PRCP
# SNOW
# TAVG
# TMAX
# TMIN
# WT01 = FOG
# WT02 = HEAVY FOG
# WT03 = THUNDER
# WT08 = SMOKE/HAZE