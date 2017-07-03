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
import utilities_modules as um
from mstats import *

# Map
map_projection = 'npstere'

# Figure 1: 12-01-75 00:00 to 12-05-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-01_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")
# print f.variables

#Initialize the date string with a value representing the beginning of the period
datenow = '1975120100'

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = i * 6 #time at or after initialization
    it = str(i_t) #making above time a string
    time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    time_str_fname = 'Hour_' + it
    #print time_str
    #mstats(temp)'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)
	
    #print PV
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

    #plt.title('Mean Sea Level Pressure at ' + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')

# Figure 2: 12-06-75 00:00 to 12-10-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-06_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-06_00:00:00', "r")
# print f.variables

i_t = 0

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = 120 + (i * 6)
    it = str(i_t)
    time_str = 'Hour ' + it
    time_str_fname = 'Hour_' + it
    #print time_str
    #print slp'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    #print PV
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

    #plt.title('Mean Sea Level Pressure at ' + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')
    

# Figure 3: 12-11-75 00:00 to 12-15-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-11_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-11_00:00:00', "r")
# print f.variables

i_t = 0

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = 240 + (i * 6)
    it = str(i_t)
    time_str = 'Hour ' + it
    time_str_fname = 'Hour_' + it
    #print time_str
    #print slp'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    #print PV
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

    #plt.title("Mean Sea Level Pressure at " + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')


# Figure 4: 12-16-75 00:00 to 12-20-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")
# print f.variables

i_t = 0

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = 360 + (i * 6)
    it = str(i_t)
    time_str = 'Hour ' + it
    time_str_fname = 'Hour_' + it
    #print time_str
    #print slp'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    #print PV
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

    #plt.title("Mean Sea Level Pressure at " + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')


# Figure 5: 12-21-75 00:00 to 12-25-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-21_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-21_00:00:00', "r")
# print f.variables

i_t = 0

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = 480 + (i * 6)
    it = str(i_t)
    time_str = 'Hour ' + it
    time_str_fname = 'Hour_' + it
    #print time_str
    #print slp'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    #print PV
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

    #plt.title("Mean Sea Level Pressure at " + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')


# Figure 6: 12-26-75 00:00 to 12-30-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-26_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-26_00:00:00', "r")
# print f.variables

i_t = 0

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = 600 + (i * 6)
    it = str(i_t)
    time_str = 'Hour ' + it
    time_str_fname = 'Hour_' + it
    #print time_str
    #print slp'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    #print PV
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

    #plt.title("Mean Sea Level Pressure at " + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')


# Figure 7: 12-31-75 00:00 to unknown
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-31_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-31_00:00:00', "r")
# print f.variables

i_t = 0

for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    temp = f1.variables['T2'][i,:,:].squeeze()
    '''i_t = 720 + (i * 6)
    it = str(i_t)
    time_str = 'Hour ' + it
    time_str_fname = 'Hour_' + it
    #print time_str'''
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    #print PV
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

    #plt.title("Mean Sea Level Pressure at " + time_str)
    plt.title('Mean Sea Level Pressure at ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/SLP/' + 'SLP' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/SLP/' + titletext + '_SLP', bbox_inches='tight')


#plt.show()
