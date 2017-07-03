#!/usr/bin/python

# imports
import netCDF4

import os, datetime, pylab
import numpy as np
import matplotlib as mpl

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid

# Add a couple of user defined functions
import weather_modules as wm
import utilities_modules_update as um
from mstats import *

# Map
map_projection = 'npstere'

#Initialize the date string with a value representing the beginning of the period
datenow = '1975120100'

# Figure 1: 12-01-75 00:00 to 12-05-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-01_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")

height = f.variables['PRES'][1,3,:,:].squeeze()
print height
