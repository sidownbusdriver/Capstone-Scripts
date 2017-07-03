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

# This script will compute advection of vorticity by the thermal wind #########

# Map
map_projection = 'npstere'

#Initialize the date string with a value representing the beginning of the period
datenow = '1975120100'

# Figure 1: 12-01-75 00:00 to 12-05-75 23:59
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-01_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)
    
    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)    

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')


# Figure 2: 12-06-75 00:00 to 12-10-75 23:59
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-06_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-06_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)

    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')


# Figure 3: 12-11-75 00:00 to 12-15-75 23:59
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-11_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-11_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)    

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)

    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')    


# Figure 4: 12-16-75 00:00 to 12-20-75 23:59
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)

    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')  


# Figure 5: 12-21-75 00:00 to 12-25-75 23:59
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-21_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-21_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)

    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')


#Figure 6: 12-26-75 00:00 to 12-30-75 23:59
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-26_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-26_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)

    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')


# Figure 7: 12-31-75 00:00 to unknown in 1976
import netCDF4
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-31_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-31_00:00:00', "r")

# Read in variables
for i in range(20):
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    pres_level = f.variables['PRES'][i,9,:,:].squeeze()
    #print pres_level  #300hPa = 25, 500hPa = 17, 700hPa = 9
    height_up = (f.variables['PH'][i,25,:,:].squeeze()+f.variables['PHB'][i,25,:,:].squeeze())/9.81
    height_low = (f.variables['PH'][i,9,:,:].squeeze()+f.variables['PHB'][i,9,:,:].squeeze())/9.81
    u_up = f.variables['U'][i,25,:,:].squeeze()
    u_low = f.variables['U'][i,9,:,:].squeeze()
    u_five = f.variables['U'][i,17,:,:].squeeze()
    v_up = f.variables['V'][i,25,:,:].squeeze() # v wind at 300hPa
    v_low = f.variables['V'][i,9,:,:].squeeze() # v wind at 700hPa
    v_five = f.variables['V'][i,17,:,:].squeeze() # v wind at 500hPa

    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H')
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    cen_lat = float(f.CEN_LAT)
    cen_lon = float(f.CEN_LON)
    truelat1 = float(f.TRUELAT1)
    truelat2 = float(f.TRUELAT2)
    standlon = float(f.STAND_LON)

    # Compute thickness between 300 hPa and 700 hPa
    thick = height_up - height_low

    # Compute vorticity at 500 hPa
    zeta = wm.vertical_vorticity_cartesian(u_five, v_five, lat, 35000, 35000, 1)

    # Compute the thermal wind
    thermal_wind_u, thermal_wind_v = wm.thermal_wind_cartesian(thick, lat, 35000, 35000)

    # Compute advection of vorticity by thermal wind
    vort_advT = wm.hadvection_cartesian(zeta, thermal_wind_u, thermal_wind_v, 35000, 35000)
    vort_advT = vort_advT * 86400
    vort_advT = ndimage.gaussian_filter(vort_advT,0.75)
    #mstats(vort_advT)
    #exit()

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
    CS = plt.contourf(new_lon, new_lat, vort_advT, cmap=plt.cm.bwr, levels=np.arange(-2.5e-6, 2.49906e-06, 10**-7), extend='both', zorder=2)
    cbar = plt.colorbar(CS, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('s^-1 day^-1')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)

    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    plt.title('500 hPa Abs. Vorticity Advection by the Thermal Wind at ' + titletext)
    plt.savefig('/home/sea_ice/scripts/sutcliffe/' + titletext + '_thermal_vort')


