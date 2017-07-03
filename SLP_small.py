#!/usr/bin/python

# imports
import netCDF4

import os, datetime
import numpy as np
import matplotlib as mpl

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid

# Add a couple of user defined functions
import weather_modules as wm
import utilities_modules as um
from mstats import *

# Map
map_projection = 'npstere'

#Initialize the date string with a value representing the beginning of the period
#datenow = '1982012500'

# Figure 1: 1975121606
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")
# print f.variables

slp = f.variables['SLP'][1,:,:].squeeze()
lat = f.variables['XLAT'][1,:,:].squeeze()
lon = f.variables['XLONG'][1,:,:].squeeze()
print 'shape of lat is ', np.shape(lat)
print 'shape of lon is ', np.shape(lon)
temp = f1.variables['T2'][1,:,:].squeeze()
ice = f1.variables['SEAICE'][1,:,:].squeeze()
#nhrs_increment = 6
#dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
#titletext = dt.strftime('%Y%m%d%H')
#print titletext
#datenow = um.advance_time(datenow,nhrs_increment)
#print time_str
#mstats(temp)

cen_lat = float(f.CEN_LAT)
cen_lon = float(f.CEN_LON)
    
# Map
m = Basemap(projection='npstere',boundinglat=60,lon_0=cen_lon,resolution='l')

# Set map properties
golden = (np.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 16./golden), dpi=128)

# Making figure
fig = plt.figure(figsize=(8., 16./golden), dpi=128) # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Convert lat and lon
new_lon, new_lat = m(lon, lat)

# Plotting
CS = plt.contour(new_lon, new_lat, slp, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
temp_plt = ((temp - 273.15)*1.8) + 32.0 #Converting temperature from Kelvins to Farenheit for plotting purposes only
CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-66,81,3), zorder=2)
cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
cb.ax.set_xlabel('Temperature in Degrees F')

m.drawcoastlines(linewidth=2)
m.fillcontinents(color='white',lake_color='aqua', zorder=1)
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='aqua')

plt.title('Mean Sea Level Pressure at 1975121606')
plt.savefig('/home/sea_ice/scripts/SLP_zoom/' + '_SLPs', bbox_inches='tight')


# Figure 2: 1975121718
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")
# print f.variables

slp = f.variables['SLP'][7,:,:].squeeze()
lat = f.variables['XLAT'][7,:,:].squeeze()
lon = f.variables['XLONG'][7,:,:].squeeze()
temp = f1.variables['T2'][7,:,:].squeeze()
ice = f1.variables['SEAICE'][7,:,:].squeeze()
#nhrs_increment = 6
#dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
#titletext = dt.strftime('%Y%m%d%H')
#print titletext
#datenow = um.advance_time(datenow,nhrs_increment)
#print time_str
#mstats(temp)

cen_lat = float(f.CEN_LAT)
cen_lon = float(f.CEN_LON)
    
# Map
m = Basemap(projection='npstere',boundinglat=60,lon_0=cen_lon,resolution='l')

# Set map properties
golden = (np.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 16./golden), dpi=128)

# Making figure
fig = plt.figure(figsize=(8., 16./golden), dpi=128) # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Convert lat and lon
new_lon, new_lat = m(lon, lat)

# Plotting
CS = plt.contour(new_lon, new_lat, slp, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
temp_plt = ((temp - 273.15)*1.8) + 32.0 #Converting temperature from Kelvins to Farenheit for plotting purposes only
CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-66,81,3), zorder=2)
cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
cb.ax.set_xlabel('Temperature in Degrees F')

m.drawcoastlines(linewidth=2)
m.fillcontinents(color='white',lake_color='aqua', zorder=1)
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='aqua')

plt.title('Mean Sea Level Pressure at 1975121718')
plt.savefig('/home/sea_ice/scripts/SLP_zoom/' + '_SLPs2', bbox_inches='tight')


# Figure 2: 1975121818
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")
# print f.variables

slp = f.variables['SLP'][11,:,:].squeeze()
lat = f.variables['XLAT'][11,:,:].squeeze()
lon = f.variables['XLONG'][11,:,:].squeeze()
temp = f1.variables['T2'][11,:,:].squeeze()
ice = f1.variables['SEAICE'][11,:,:].squeeze()
#nhrs_increment = 6
#dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
#titletext = dt.strftime('%Y%m%d%H')
#print titletext
#datenow = um.advance_time(datenow,nhrs_increment)
#print time_str
#mstats(temp)

cen_lat = float(f.CEN_LAT)
cen_lon = float(f.CEN_LON)
    
# Map
m = Basemap(projection='npstere',boundinglat=60,lon_0=cen_lon,resolution='l')

# Set map properties
golden = (np.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 16./golden), dpi=128)

# Making figure
fig = plt.figure(figsize=(8., 16./golden), dpi=128) # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Convert lat and lon
new_lon, new_lat = m(lon, lat)

# Plotting
CS = plt.contour(new_lon, new_lat, slp, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
temp_plt = ((temp - 273.15)*1.8) + 32.0 #Converting temperature from Kelvins to Farenheit for plotting purposes only
CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-66,81,3), zorder=2)
cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
cb.ax.set_xlabel('Temperature in Degrees F')

m.drawcoastlines(linewidth=2)
m.fillcontinents(color='white',lake_color='aqua', zorder=1)
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='aqua')

plt.title('Mean Sea Level Pressure at 1975121818')
plt.savefig('/home/sea_ice/scripts/SLP_zoom/' + '_SLPs3', bbox_inches='tight')
