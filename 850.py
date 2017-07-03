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

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')


# Figure 2: 12-06-75 00:00 to 12-10-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-06_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-06_00:00:00', "r")

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')


# Figure 3: 12-11-75 00:00 to 12-15-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-11_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-11_00:00:00', "r")

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')


# Figure 4: 12-16-75 00:00 to 12-20-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')


# Figure 5: 12-21-75 00:00 to 12-25-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-21_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-21_00:00:00', "r")

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')


#Figure 6: 12-26-75 00:00 to 12-30-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-26_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-26_00:00:00', "r")

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')


# Figure 7: 12-31-75 00:00 to unknown in 1976
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-31_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-31_00:00:00', "r")

# For loop
for i in range(20):
    height = (f.variables['PH'][i,3,:,:].squeeze()+f.variables['PHB'][i,3,:,:].squeeze())/9.81
    temp = f.variables['T'][i,3,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # BEGIN ACTUAL PROCESSING HERE
    # x_dim and y_dim are the x and y dimensions of the model
    # domain in gridpoints
    #x_dim = len(nc.dimensions['west_east'])
    #y_dim = len(nc.dimensions['south_north'])

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    #width_meters = dx * (x_dim - 1)
    #height_meters = dy * (y_dim - 1)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Convert temperatures to Farenheit 
    temp_plt = ((temp - 273.15)*1.8) + 32.0

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
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, temp_plt, range(-50,60,3), zorder=2)
    cb = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cb.ax.set_xlabel('Temperature in Degrees F')

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('850 hPa Geopotential Height and Temperature at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/850/' + titletext + '_height')
    

# plt.show()
    





    

