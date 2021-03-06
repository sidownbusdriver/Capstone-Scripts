# Cross Sections with Python
# 
# -----
# 
# Quick routine to generate cross sections with Python
# 
# Steven Cavallo
# Adapted from Patrick Marsh
# March 2013
#Modified by Curtis Riganti, Aaron Hardin and Parker Brown to make cross sections for different variables
#For this version of the script, we plot temperature advection
#June 2013

###############################################################
# Imports
###############################################################

import os
import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import weather_modules as wm

import utilities_modules_update as um
from mstats import *
from scipy import ndimage

###############################################################
# Cross Section 1
###############################################################
fpath = '/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00'
level2plot = 500      # Level to plot (hPa)
timeindex = 1       # Time index to plot
slat, slon = 75, -138   # starting latitude,longitude pair of cross section.  Use negative longitudes for Western Hemisphere. 
elat, elon = 74, 35  # ending latitude,longitude pair of cross section.  Use negative longitudes for Western Hemisphere.

nc = netCDF4.Dataset(fpath, 'r')
hgt = nc.variables['PRES'][0,:,0,0].squeeze()
u_wind = nc.variables['U'][timeindex,:,:,:].squeeze() #Pulling in u wind for advection
v_wind = nc.variables['V'][timeindex,:,:,:].squeeze() #Pulling in v wind for advection
theta = nc.variables['TH'][timeindex,:,:,:].squeeze()
trop = nc.variables['EPV'][timeindex,:,:,:].squeeze()
levelindex = np.ravel(hgt==level2plot)
tmp = nc.variables['T'][timeindex,:,:,:].squeeze() # Cross section variable.  Chose temperature as an example here.
slp = nc.variables['SLP'][timeindex,:,:].squeeze()
lons = nc.variables['XLONG'][0,:,:].squeeze()
lats = nc.variables['XLAT'][0,:,:].squeeze()
tadv = np.zeros_like(tmp).astype('f')

#Compute temperature advection over the depth of the model using hadvection from weather_modules
for i in range(32):
    temp = tmp[i,:,:]
    u_wind2 = u_wind[i,:,:]
    v_wind2 = v_wind[i,:,:]
    tadv[i,:,:] = wm.hadvection_cartesian(temp,u_wind2,v_wind2,35000,35000) #Changed u_wind to u_wind2, ditto for v_wind
    print 'the shape of tadv is', np.shape(tadv)
tadv = tadv * 86400

cen_lon = float(nc.CEN_LON)

nc.close

# Create a basemap instance. This allows for the cross section to be conducted in the appropriate projection
m = Basemap(projection='npstere',boundinglat=47,lon_0=cen_lon,resolution='l')
# Get the cross section points.  This is a function in utilities_modules.
xx, yy = um.xsection_inds(slon, slat, elon, elat, lons, lats, m)


x, y = m(lons, lats)
clevs1 = np.arange(220, 260, 1)
clevs2 = np.arange(260, 350, 2)
slplevs = np.arange(948,1000,4)
slp_ticks = slplevs[::2]
trop_level = [2.0,2.0]

golden = (np.sqrt(5)+1.)/2.

# Plot plan view map with solid white line indicating the location of the cross section
fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
ax0 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
F = plt.gcf()  # Gets the current figure


#m.drawstates(color='#444444', linewidth=1.25)
m.drawcoastlines(linewidth=1.25)
m.fillcontinents(color='peru',lake_color='aqua', zorder=1)
#m.drawcountries(color='#444444', linewidth=1.25)
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='aqua')


#plotvar = tmp[levelindex,:,:].squeeze()
#cbar0 = ax0.contourf(x, y, plotvar, levels=clevs1)
#plt.colorbar(cbar0, orientation='horizontal')
#cbar1 = ax0.contour(x, y, slp, levels=slplevs,colors='k', linewidths=1.0)
#plt.clabel(cbar1,slp_ticks, fmt = '%i', inline=True, fontsize=10)
ax0.plot(x[xx,yy], y[xx,yy], color='w', lw=4)
ax0.plot([x[xx[0],yy[0]], x[xx[-1],yy[-1]]], [y[xx[0],yy[0]], y[xx[-1],yy[-1]]], color='w', lw=2, ls=":")
ax0.title.set_y(1.00)
ax0.set_title('Area of Cross Section at 1975121606', size=20)

plt.savefig('/home/sea_ice/scripts/CrossSections/' + '20area1_tadv', bbox_inches='tight')


# Cross section on log-p space
fig = plt.figure(figsize=(12., 12./golden), dpi=128)   # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.82])

F = plt.gcf()  # Gets the current figure

# Smooth out potential temperature
theta2 = theta[:,xx,yy]
#theta2[0:2,:] = float('NaN')
theta2[2:] = ndimage.gaussian_filter(theta2[2:],.75)
trop2 = trop[:,xx,yy]
trop2 = um.filter_numeric_nans(trop2,1000,0,'high')
tadv2 =tadv[:,xx,yy]
#mstats(trop2)
trop2[0:6,:] = float('NaN')
trop2 = ndimage.gaussian_filter(trop2,1)

tx = range(xx.shape[0])
ty = hgt
ttxx, ttyy = np.meshgrid(tx, ty)
#CS1 = ax1.contourf(ttxx, ttyy, theta2,cmap=plt.cm.jet,levels=clevs2)
#CS2 = ax1.contour(ttxx, ttyy, theta2,colors='k',linewidths=1,levels=clevs2)
CS3 = ax1.contour(ttxx, ttyy, trop2,colors='k',linewidths=3,levels=trop_level)
CS4 = ax1.contourf(ttxx,ttyy,tadv2, cmap = plt.cm.RdBu_r, levels= np.arange(-75,80,5))
cbar = plt.colorbar(CS4, shrink=0.95, orientation='horizontal',extend='both',pad=.16)
cbar.set_label('Kelvins/Day')
#plt.clabel(CS4, inline=1)
labs = []
for xxx,yyy in zip(xx,yy):
    labs.append('%.1f, %.1f' % (lats[xxx,yyy], lons[xxx,yyy]))
ax1.set_xticks(np.arange(0,xx.shape[0]+1e-11, 5))
ax1.set_xticklabels(labs[0::5], rotation=60);
yticks = [1000, 925, 850, 700, 500, 300, 250, 200, 150, 100]
ax1.semilogy()
ax1.set_ylim(925, 150)
ax1.set_yticks(yticks)
ax1.set_yticklabels(yticks)
ax1.set_ylim(925, 150)

ax0.title.set_y(1.05)
#ax0.set_title('Potential Temperature (K)', size=20)
#ax1.title.set_y(1.05)
ax1.set_title('Temperature Advection Cross Section at 1975121606', size=20)
ax1.grid(axis='y', ls=':', lw=2)

plt.savefig('/home/sea_ice/scripts/CrossSections/' + '20cross1_tadv', bbox_inches='tight')



##### Cross Section 2 ################################################################
fpath = '/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00'
level2plot = 500      # Level to plot (hPa)
timeindex = 7       # Time index to plot
slat, slon = 77, -170   # starting latitude,longitude pair of cross section.  Use negative longitudes for Western Hemisphere. 
elat, elon = 75, 75  # ending latitude,longitude pair of cross section.  Use negative longitudes for Western Hemisphere.

nc = netCDF4.Dataset(fpath, 'r')
hgt = nc.variables['PRES'][0,:,0,0].squeeze()
u_wind = nc.variables['U'][timeindex,:,:,:].squeeze() #Pulling in u wind for advection
v_wind = nc.variables['V'][timeindex,:,:,:].squeeze() #Pulling in v wind for advection
theta = nc.variables['TH'][timeindex,:,:,:].squeeze()
trop = nc.variables['EPV'][timeindex,:,:,:].squeeze()
levelindex = np.ravel(hgt==level2plot)
tmp = nc.variables['T'][timeindex,:,:,:].squeeze() # Cross section variable.  Chose temperature as an example here.
slp = nc.variables['SLP'][timeindex,:,:].squeeze()
lons = nc.variables['XLONG'][0,:,:].squeeze()
lats = nc.variables['XLAT'][0,:,:].squeeze()
tadv = np.zeros_like(tmp).astype('f')

#Compute temperature advection over the depth of the model using hadvection from weather_modules
for i in range(32):
    temp = tmp[i,:,:]
    u_wind2 = u_wind[i,:,:]
    v_wind2 = v_wind[i,:,:]
    tadv[i,:,:] = wm.hadvection_cartesian(temp,u_wind2,v_wind2,35000,35000) #Changed u_wind to u_wind2, ditto for v_wind
    #print 'the shape of tadv is', np.shape(tadv)
tadv = tadv * 86400

cen_lon = float(nc.CEN_LON)

nc.close


# Create a basemap instance. This allows for the cross section to be conducted in the appropriate projection
m = Basemap(projection='npstere',boundinglat=47,lon_0=cen_lon,resolution='l')
# Get the cross section points.  This is a function in utilities_modules.
xx, yy = um.xsection_inds(slon, slat, elon, elat, lons, lats, m)


x, y = m(lons, lats)
clevs1 = np.arange(220, 260, 1)
clevs2 = np.arange(260, 350, 2)
slplevs = np.arange(948,1000,4)
slp_ticks = slplevs[::2]
trop_level = [2.0,2.0]

golden = (np.sqrt(5)+1.)/2.

# Plot plan view map with solid white line indicating the location of the cross section
fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
ax0 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
F = plt.gcf()  # Gets the current figure


#m.drawstates(color='#444444', linewidth=1.25)
m.drawcoastlines(linewidth=1.25)
m.fillcontinents(color='peru',lake_color='aqua', zorder=1)
#m.drawcountries(color='#444444', linewidth=1.25)
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='aqua')


#plotvar = tmp[levelindex,:,:].squeeze()
#cbar0 = ax0.contourf(x, y, plotvar, levels=clevs1)
#plt.colorbar(cbar0, orientation='horizontal')
#cbar1 = ax0.contour(x, y, slp, levels=slplevs,colors='k', linewidths=1.0)
#plt.clabel(cbar1,slp_ticks, fmt = '%i', inline=True, fontsize=10)
ax0.plot(x[xx,yy], y[xx,yy], color='w', lw=4)
ax0.plot([x[xx[0],yy[0]], x[xx[-1],yy[-1]]], [y[xx[0],yy[0]], y[xx[-1],yy[-1]]], color='w', lw=2, ls=":")
ax0.title.set_y(1.00)
ax0.set_title('Area of Cross Section at 1975121718', size=20)

plt.savefig('/home/sea_ice/scripts/CrossSections/' + '20area2_tadv', bbox_inches='tight')


# Cross section on log-p space
fig = plt.figure(figsize=(12., 12./golden), dpi=128)   # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.82])

F = plt.gcf()  # Gets the current figure

# Smooth out potential temperature
theta2 = theta[:,xx,yy]
#theta2[0:2,:] = float('NaN')
theta2[2:] = ndimage.gaussian_filter(theta2[2:],.75)
trop2 = trop[:,xx,yy]
trop2 = um.filter_numeric_nans(trop2,1000,0,'high')
tadv2 =tadv[:,xx,yy]
#mstats(trop2)
trop2[0:6,:] = float('NaN')
trop2 = ndimage.gaussian_filter(trop2,1)

tx = range(xx.shape[0])
ty = hgt
ttxx, ttyy = np.meshgrid(tx, ty)
#CS1 = ax1.contourf(ttxx, ttyy, theta2,cmap=plt.cm.jet,levels=clevs2)
#CS2 = ax1.contour(ttxx, ttyy, theta2,colors='k',linewidths=1,levels=clevs2)
CS3 = ax1.contour(ttxx, ttyy, trop2,colors='k',linewidths=3,levels=trop_level)
CS4 = ax1.contourf(ttxx,ttyy,tadv2, cmap = plt.cm.RdBu_r, levels= np.arange(-75,80,5))
cbar = plt.colorbar(CS4, shrink=0.95, orientation='horizontal',extend='both',pad=.16)
cbar.set_label('Kelvins/Day')
#plt.clabel(CS4, inline=1)
labs = []
for xxx,yyy in zip(xx,yy):
    labs.append('%.1f, %.1f' % (lats[xxx,yyy], lons[xxx,yyy]))
ax1.set_xticks(np.arange(0,xx.shape[0]+1e-11, 5))
ax1.set_xticklabels(labs[0::5], rotation=60);
yticks = [1000, 925, 850, 700, 500, 300, 250, 200, 150, 100]
ax1.semilogy()
ax1.set_ylim(925, 150)
ax1.set_yticks(yticks)
ax1.set_yticklabels(yticks)
ax1.set_ylim(925, 150)

ax0.title.set_y(1.05)
#ax0.set_title('Potential Temperature (K)', size=20)
#ax1.title.set_y(1.05)
ax1.set_title('Temperature Advection Cross Section at 1975121718', size=20)
ax1.grid(axis='y', ls=':', lw=2)

plt.savefig('/home/sea_ice/scripts/CrossSections/' + '20cross2_tadv', bbox_inches='tight')


######## Cross Section 3 ########################################################
fpath = '/archive/capstone/sea_ice/wrfout_pres_1975-12-16_00:00:00'
level2plot = 500      # Level to plot (hPa)
timeindex = 11       # Time index to plot74,1
slat, slon = 67, 75   # starting latitude,longitude pair of cross section.  Use negative longitudes for Western Hemisphere. 
elat, elon = 74, 1  # ending latitude,longitude pair of cross section.  Use negative longitudes for Western Hemisphere.

nc = netCDF4.Dataset(fpath, 'r')
hgt = nc.variables['PRES'][0,:,0,0].squeeze()
u_wind = nc.variables['U'][timeindex,:,:,:].squeeze() #Pulling in u wind for advection
v_wind = nc.variables['V'][timeindex,:,:,:].squeeze() #Pulling in v wind for advection
theta = nc.variables['TH'][timeindex,:,:,:].squeeze()
trop = nc.variables['EPV'][timeindex,:,:,:].squeeze()
levelindex = np.ravel(hgt==level2plot)
tmp = nc.variables['T'][timeindex,:,:,:].squeeze() # Cross section variable.  Chose temperature as an example here.
slp = nc.variables['SLP'][timeindex,:,:].squeeze()
lons = nc.variables['XLONG'][0,:,:].squeeze()
lats = nc.variables['XLAT'][0,:,:].squeeze()
tadv = np.zeros_like(tmp).astype('f')

#Compute temperature advection over the depth of the model using hadvection from weather_modules
for i in range(32):
    temp = tmp[i,:,:]
    u_wind2 = u_wind[i,:,:]
    v_wind2 = v_wind[i,:,:]
    tadv[i,:,:] = wm.hadvection_cartesian(temp,u_wind2,v_wind2,35000,35000) #Changed u_wind to u_wind2, ditto for v_wind
    #print 'the shape of tadv is', np.shape(tadv)
tadv = tadv * 86400

cen_lon = float(nc.CEN_LON)

nc.close


# Create a basemap instance. This allows for the cross section to be conducted in the appropriate projection
m = Basemap(projection='npstere',boundinglat=47,lon_0=cen_lon,resolution='l')
# Get the cross section points.  This is a function in utilities_modules.
xx, yy = um.xsection_inds(slon, slat, elon, elat, lons, lats, m)


x, y = m(lons, lats)
clevs1 = np.arange(220, 260, 1)
clevs2 = np.arange(260, 350, 2)
slplevs = np.arange(948,1000,4)
slp_ticks = slplevs[::2]
trop_level = [2.0,2.0]

golden = (np.sqrt(5)+1.)/2.

# Plot plan view map with solid white line indicating the location of the cross section
fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
ax0 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
F = plt.gcf()  # Gets the current figure


#m.drawstates(color='#444444', linewidth=1.25)
m.drawcoastlines(linewidth=1.25)
m.fillcontinents(color='peru',lake_color='aqua', zorder=1)
#m.drawcountries(color='#444444', linewidth=1.25)
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='aqua')


#plotvar = tmp[levelindex,:,:].squeeze()
#cbar0 = ax0.contourf(x, y, plotvar, levels=clevs1)
#plt.colorbar(cbar0, orientation='horizontal')
#cbar1 = ax0.contour(x, y, slp, levels=slplevs,colors='k', linewidths=1.0)
#plt.clabel(cbar1,slp_ticks, fmt = '%i', inline=True, fontsize=10)
ax0.plot(x[xx,yy], y[xx,yy], color='w', lw=4)
ax0.plot([x[xx[0],yy[0]], x[xx[-1],yy[-1]]], [y[xx[0],yy[0]], y[xx[-1],yy[-1]]], color='w', lw=2, ls=":")
ax0.title.set_y(1.00)
ax0.set_title('Area of Cross Section at 1975121818', size=20)

plt.savefig('/home/sea_ice/scripts/CrossSections/' + '20area3_tadv', bbox_inches='tight')


# Cross section on log-p space
fig = plt.figure(figsize=(12., 12./golden), dpi=128)   # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.82])

F = plt.gcf()  # Gets the current figure

# Smooth out potential temperature
theta2 = theta[:,xx,yy]
#theta2[0:2,:] = float('NaN')
theta2[2:] = ndimage.gaussian_filter(theta2[2:],.75)
trop2 = trop[:,xx,yy]
trop2 = um.filter_numeric_nans(trop2,1000,0,'high')
tadv2 =tadv[:,xx,yy]
#mstats(trop2)
trop2[0:6,:] = float('NaN')
trop2 = ndimage.gaussian_filter(trop2,1)

tx = range(xx.shape[0])
ty = hgt
ttxx, ttyy = np.meshgrid(tx, ty)
#CS1 = ax1.contourf(ttxx, ttyy, theta2,cmap=plt.cm.jet,levels=clevs2)
#CS2 = ax1.contour(ttxx, ttyy, theta2,colors='k',linewidths=1,levels=clevs2)
CS3 = ax1.contour(ttxx, ttyy, trop2,colors='k',linewidths=3,levels=trop_level)
CS4 = ax1.contourf(ttxx,ttyy,tadv2, cmap = plt.cm.RdBu_r, levels= np.arange(-75,80,5))
cbar = plt.colorbar(CS4, shrink=0.95, orientation='horizontal',extend='both',pad=.16)
cbar.set_label('Kelvins/Day')
#plt.clabel(CS4, inline=1)
labs = []
for xxx,yyy in zip(xx,yy):
    labs.append('%.1f, %.1f' % (lats[xxx,yyy], lons[xxx,yyy]))
ax1.set_xticks(np.arange(0,xx.shape[0]+1e-11, 5))
ax1.set_xticklabels(labs[0::5], rotation=60);
yticks = [1000, 925, 850, 700, 500, 300, 250, 200, 150, 100]
ax1.semilogy()
ax1.set_ylim(925, 150)
ax1.set_yticks(yticks)
ax1.set_yticklabels(yticks)
ax1.set_ylim(925, 150)

ax0.title.set_y(1.05)
#ax0.set_title('Potential Temperature (K)', size=20)
#ax1.title.set_y(1.05)
ax1.set_title('Temperature Advection Cross Section at 1975121818', size=20)
ax1.grid(axis='y', ls=':', lw=2)

plt.savefig('/home/sea_ice/scripts/CrossSections/' + '20cross3_tadv', bbox_inches='tight')




