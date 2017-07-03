#!/usr/bin/python

# imports
import netCDF4

import os, datetime, pylab
import numpy as np
import matplotlib as mpl
from scipy import ndimage

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid

# Add a couple of user defined functions
import weather_modules as wm
import utilities_modules_update as um
from mstats import *

# Map
map_projection = 'npstere'

# Figure 1: 12-01-75 00:00 to 12-05-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-01_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")

#Initialize the date string with a value representing the beginning of the period
datenow = '1975120100'

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


# Figure 2: 12-06-75 00:00 to 12-10-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-06_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-06_00:00:00', "r")

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


# Figure 3: 12-11-75 00:00 to 12-15-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-11_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-11_00:00:00', "r")

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


# Figure 4: 12-16-75 00:00 to 12-20-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


# Figure 5: 12-21-75 00:00 to 12-25-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-21_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-21_00:00:00', "r")

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


#Figure 6: 12-26-75 00:00 to 12-30-75 23:59
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-26_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-26_00:00:00', "r")

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


# Figure 7: 12-31-75 00:00 to unknown in 1976
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-31_00:00:00', "r")
f1 = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-31_00:00:00', "r")

#For Loop which creates plots while iterating through time steps in the NetCDF file

for i in range(20):
    u_top = f.variables['U'][i,21,:,:].squeeze()
    v_top = f.variables['V'][i,21,:,:].squeeze()
    u_bot = f.variables['U'][i,9,:,:].squeeze()
    v_bot = f.variables['V'][i,9,:,:].squeeze()
    #pres = f.variables['PRES'][i,21,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #print pres
    
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Get the grid spacing
    dx = float(f.DX)
    dy = float(f.DY)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    f.close
    f1.close

    # Compute vorticity
    zeta1 = wm.vertical_vorticity_cartesian(u_top, v_top, lat, 35000, 35000, 1)
    zeta2 = wm.vertical_vorticity_cartesian(u_bot, v_bot, lat, 35000, 35000, 1)

    # Compute vorticity advection
    vort_adv1 = wm.hadvection_cartesian(zeta1, u_top, v_top, 35000, 35000)
    vort_adv2 = wm.hadvection_cartesian(zeta1, u_bot, v_bot, 35000, 35000)

    # Compute differential voriticty advection
    diff_vort = vort_adv1 - vort_adv2
    diff_vort = ndimage.gaussian_filter(diff_vort,2.0)
    
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
    CS = plt.contourf(new_lon, new_lat, diff_vort, cmap=plt.cm.bwr, levels=np.arange(-9*10**-10, 9.1*10**-10, 1*10**-11), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/second^2')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('400 to 700 (hPa) Differential Vorticity Advection at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/differential_vorticity/' + titletext + '_diff_vort')


#plt.show()









