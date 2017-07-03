#!/usr/bin/python

# imports
import netCDF4 as nc
#import netCDF4
import os, datetime
import numpy as np
import matplotlib as mpl

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid
from scipy import ndimage

# Add a couple of user defined functions
import weather_modules as wm
import utilities_modules_update as um
from mstats import *

# Map
map_projection = 'npstere'

#Initialize the date string with a value representing the beginning of the period
datenow = '1975120100'

# Figure 1: 12-00-75 00:00 to 12-05-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-01_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")
# print f.variables

# For loop
for i in range(2):
    omega = f.variables['W'][i,17,:,:].squeeze()
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    vapor = f.variables['QVAPOR'][i,17,:,:].squeeze()
    T = f.variables['T'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    '''i_t = i * 6 #time at or after initialization
    it = str(i_t) #making above time a string
    time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    time_str_fname = 'Hour_' + it
    #print vapor'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)
    
    # Compute omega
    density = 50000./(287.*T*(1+(.61*vapor)))
    omega = (-density)*9.81*omega
    #print density

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    # Map
    m = Basemap(projection='npstere',boundinglat=47,lon_0=cen_lon,resolution='l')

    # Set map properties
    golden = (np.sqrt(5)+1.)/2.
    figprops = dict(figsize=(8., 16./golden), dpi=128)

    # Making figure
    fig = plt.figure(figsize=(8., 16./golden), dpi=128) # New figure
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # Convert lat and lon
    new_lon, new_lat = m(lon, lat)
    
    # Smoothing omega for plotting
    omega_smooth = ndimage.gaussian_filter(omega, 2.5)

    # Plotting
    CS = plt.contourf(new_lon, new_lat, omega_smooth , cmap=plt.cm.bwr, levels=np.arange(-.2, .2, .025), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Pa/s')
    CS3 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines()
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Omega ' + time_str)
    plt.title('500 hPa Omega at ' + titletext)
    #plt.savefig('Omega' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/omega/' + titletext + '_H5_Omega_sm')

#plt.show()
