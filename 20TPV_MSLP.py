#!/usr/bin/python

# imports
import netCDF4

import os, datetime
import numpy as np
import matplotlib as mpl
import netCDF4 as nc
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

# Figures Part 1: 12-00-75 00:00 to 12-05-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-01_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")
# print f.variables

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    '''i_t = i * 6 #time at or after initialization
    it = str(i_t) #making above time a string
    time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)'''
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
    CS = plt.contourf(new_lon, new_lat, pot_temp, cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Tropopause Potential Temperature at ' + time_str)
    plt.title('Potential Temperature at 2PVU ' + titletext)
    #plt.savefig('/home/sea_ice/scripts/TPV/' + 'TPV' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')

      
#Figures Part 2: 12-06-75 00:00 to 12-10-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-06_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-06_00:00:00', "r")

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = 120 + (i * 6) #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)
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
    CS = plt.contourf(new_lon, new_lat, pot_temp , cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('Potential Temperature at 2PVU ' + titletext)
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')


#Figures Part 3: 12-11-75 00:00 to 12-15-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-11_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-11_00:00:00', "r")

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = 120 + (i * 6) #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)
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
    CS = plt.contourf(new_lon, new_lat, pot_temp , cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('Potential Temperature at 2PVU ' + titletext)
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')


#Figures Part 4: 12-16-75 00:00 to 12-20-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-16_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = 120 + (i * 6) #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)
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
    CS = plt.contourf(new_lon, new_lat, pot_temp , cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('Potential Temperature at 2PVU ' + titletext)
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')


#Figures Part 5: 12-21-75 00:00 to 12-25-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-21_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-21_00:00:00', "r")

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = 120 + (i * 6) #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)
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
    CS = plt.contourf(new_lon, new_lat, pot_temp , cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('Potential Temperature at 2PVU ' + titletext)
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')


#Figures Part 6: 12-26-75 00:00 to 12-30-75 23:59
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-26_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-26_00:00:00', "r")

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = 120 + (i * 6) #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)
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
    CS = plt.contourf(new_lon, new_lat, pot_temp , cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('Potential Temperature at 2PVU ' + titletext)
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')


#Figures Part 7: 12-31-75 00:00 to end
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_trop_1975-12-31_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-31_00:00:00', "r")

# For loop
for i in range(20):
    slp = f.variables['SLP'][i,:,:].squeeze()
    pot_temp = f.variables['THETA'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = 120 + (i * 6) #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    # print np.max(pot_temp)
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
    CS = plt.contourf(new_lon, new_lat, pot_temp , cmap=plt.cm.jet, levels=np.arange(280, 355, 4), extend='both', zorder=2)
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contour(new_lon, new_lat, slp, colors='k', levels=np.arange(964,1041,4), linewidths=1.5, linestyle='solid', zorder=4)
    CS3label = plt.clabel(CS3, inline=1, fontsize=10, fmt='%1.0f')
    cb = plt.colorbar(CS, shrink=.95, orientation = "horizontal", extend='both', pad=.05)
    cb.ax.set_xlabel('Potential Temperature in Kelvins')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('Potential Temperature at 2PVU ' + titletext)
    plt.savefig('/home/sea_ice/scripts/MSLP_TPV/' + titletext + '_MSLP_tpTheta', bbox_inches='tight')


