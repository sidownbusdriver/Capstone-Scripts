# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

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

#from mstats import *

import warnings
warnings.filterwarnings("ignore")



# Set the default domain to be d02
level2plot = 500
timeindex = 10
fpath = '/home/scavallo/data/wrfout_pres_1982-02-04_00:00:00'
TITLESTRING = 'WRF Polar plot'
# Thin factor is used for thinning out wind barbs
thin = 10


##################################################################
nc = netCDF4.Dataset(fpath,'r')
# Grab these variables for now
levs = nc.variables['PRES'][0,:,0,0].squeeze()
levelindex = np.ravel(levs==level2plot)
print levs[levelindex]

u_grid = nc.variables['U'][timeindex,levelindex,:,:].squeeze()
v_grid = nc.variables['V'][timeindex,levelindex,:,:].squeeze()
ghgt = (nc.variables['PH'][timeindex,levelindex,:,:].squeeze() + nc.variables['PHB'][timeindex,levelindex,:,:].squeeze())/9.81
T = nc.variables['T'][timeindex,levelindex,:,:].squeeze()
xlat = nc.variables['XLAT'][0,:,:].squeeze()
xlon = nc.variables['XLONG'][0,:,:].squeeze()



# BEGIN ACTUAL PROCESSING HERE
# x_dim and y_dim are the x and y dimensions of the model
# domain in gridpoints
x_dim = len(nc.dimensions['west_east'])
y_dim = len(nc.dimensions['south_north'])

# Get the grid spacing
dx = float(nc.DX)
dy = float(nc.DY)

width_meters = dx * (x_dim - 1)
height_meters = dy * (y_dim - 1)

cen_lat = float(nc.CEN_LAT)
cen_lon = float(nc.CEN_LON)
truelat1 = float(nc.TRUELAT1)
truelat2 = float(nc.TRUELAT2)
standlon = float(nc.STAND_LON)

[ut,vt] = um.grid_to_true_wind(xlon,u_grid,v_grid,truelat1,truelat2,standlon,'polar')


nc.close

min_ghgt = 4800
max_ghgt = 6000
cint_ghgt = 60
cflevs_ghgt =  np.arange(min_ghgt, max_ghgt, cint_ghgt)
cflevs_ghgt_ticks = cflevs_ghgt
 
golden = (np.sqrt(5)+1.)/2.
fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

m = Basemap(projection='npstere',boundinglat=42,lon_0=cen_lon,resolution='l')
F = plt.gcf()  # Gets the current figure


m.drawstates(color='#444444', linewidth=1.25)
m.drawcoastlines(color='#444444')
m.drawcountries(color='#444444', linewidth=1.25)

x, y = m(xlon,xlat)
CS1 = m.contour(x, y, ghgt, cflevs_ghgt, colors='k', linewidths=1.0)
plt.clabel(CS1, cflevs_ghgt_ticks, fmt = '%i', inline=True, fontsize=10)

ut = ut * 1.94384449
vt = vt * 1.94384449

uproj,vproj,xx,yy = m.rotate_vector(ut, vt, xlon, xlat, returnxy=True)
barbs = m.barbs(xx[::thin,::thin],yy[::thin,::thin],uproj[::thin,::thin],vproj[::thin,::thin],length=5,barbcolor='k',flagcolor='r',linewidth=1.0,sizes={'spacing':0.2},pivot='middle')




plt.title('%s' % (TITLESTRING), fontsize=11,bbox=dict(facecolor='white', alpha=0.65),x=0.5,y=.95,weight = 'demibold',style='oblique', \
		stretch='normal', family='sans-serif')
plt.show()




