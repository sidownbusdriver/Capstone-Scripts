#!/usr/bin/python

# imports
import netCDF4

import os, datetime
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

#Initialize the date string with a value representing the beginning of the period
datenow = '1975120100'

# Figure 1: 12-01-75 00:00 to 12-05-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-01_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = i * 6 #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()

# Figure 2: 12-06-75 00:00 to 12-10-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-06_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-06_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = i * 6 #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both',pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()

# Figure 3: 12-11-75 00:00 to 12-15-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-11_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-11_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = i * 6 #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()

# Figure 4: 12-16-75 00:00 to 12-20-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-16_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = i * 6 #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()

# Figure 5: 12-21-75 00:00 to 12-25-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-21_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-21_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    #i_t = i * 6 #time at or after initialization
    #it = str(i_t) #making above time a string
    #time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    #time_str_fname = 'Hour_' + it
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()

#TEMPORARY DATENOW DECLARATION
datenow = '1975122600'

#Figure 6: 12-26-75 00:00 to 12-30-75 23:59
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-26_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-26_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    '''i_t = i * 6 #time at or after initialization
    it = str(i_t) #making above time a string
    time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    time_str_fname = 'Hour_' + it'''
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()

# Figure 7: 12-31-75 00:00 to unknown in 1976
import netCDF4 
f = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_pres_1975-12-31_00:00:00', "r")
f1 = netCDF4.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-31_00:00:00', "r")

#For loop
for i in range(20):
    height = (f.variables['PH'][i,17,:,:].squeeze()+f.variables['PHB'][i,17,:,:].squeeze())/9.81
    u_wind = f.variables['U'][i,17,:,:].squeeze()
    v_wind = f.variables['V'][i,17,:,:].squeeze()
    lat = f.variables['XLAT'][i,:,:].squeeze()
    lon = f.variables['XLONG'][i,:,:].squeeze()
    ice = f1.variables['SEAICE'][i,:,:].squeeze()
    '''i_t = i * 6 #time at or after initialization
    it = str(i_t) #making above time a string
    time_str = 'Hour ' + it #creating a string to be used later that has time after initialization info
    time_str_fname = 'Hour_' + it'''
    #print height
    nhrs_increment = 6
    dt = datetime.datetime.strptime(datenow, '%Y%m%d%H') 
    titletext = dt.strftime('%Y%m%d%H')
    #print titletext
    datenow = um.advance_time(datenow,nhrs_increment)

    # Convert winds to knots
    u_wind = u_wind*1.943
    v_wind = v_wind*1.943
    
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

    [ut,vt] = um.grid_to_true_wind(lon,u_wind,v_wind,truelat1,truelat2,standlon,'polar')
    f.close
    f1.close
    
    # Compute voritcity
    zeta = wm.vertical_vorticity_cartesian(u_wind, v_wind, lat, 35000, 35000, 1)
    zeta = ndimage.gaussian_filter(zeta,0.75)

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

    # Convert winds
    uproj,vproj,xx,yy = m.rotate_vector(ut, vt, lon, lat, returnxy=True)
	 
    # Plotting
    CS = plt.contour(new_lon, new_lat, height, 20, colors='k', linewidths=1.5, linestyle='solid', zorder=4)
    CL = plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
    CS2 = plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=5.0, linestyle='solid', zorder=3)
    barbs = m.barbs(xx[::10,::10],yy[::10,::10],uproj[::10,::10],vproj[::10,::10],length=5,barbcolor='k',flagcolor='r',linewidth=1.0, zorder=3)
    CS3 = plt.contourf(new_lon, new_lat, zeta, cmap=plt.cm.hot_r, levels=np.arange(15*10**-5, 40*10**-5, 1*10**-5), extend='both', zorder=2)
    cbar = plt.colorbar(CS3, shrink=.95, orientation='horizontal', extend='both', pad=.05)
    cbar.ax.set_xlabel('1/s')
 
    m.drawcoastlines(linewidth=2)
    m.fillcontinents(color='white',lake_color='aqua', zorder=1)
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,10.))
    m.drawmeridians(np.arange(-180.,181.,10.))
    m.drawmapboundary(fill_color='aqua')

    #plt.title('Geopotential Height, Wind, and Vertical Vorticity at ' + time_str)
    plt.title('500 hPa Geopotential Height, Wind, and Vertical Vorticity at ' + titletext)
    #plt.savefig('height' + time_str_fname, bbox_inches='tight')
    plt.savefig('/home/sea_ice/scripts/500/' + titletext + '_height')


#plt.show()
