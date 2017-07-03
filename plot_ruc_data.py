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

#from mstats import *

import warnings
warnings.filterwarnings("ignore")
###################################
# Set user options
###################################
map_projection = 'lcc' # 'ortho' for orthographic projection, 'lcc' for Lambert Conformal projection
level2plot = [50000]
deltax = 20000 # 20 km
figname = "ruc_test" # will save an image named this with a .png extension



# Now provide the path to the directory containing the .nc file. Please note,
# do NOT include the .nc file in the path.
fpath = '/home/xxxx/data/rap_252_20121106_0000_000.nc'

###################################
# END user options
###################################
f = netCDF4.Dataset(fpath,'r')
lons = f.variables['gridlon_0'][:,:]
lats = f.variables['gridlat_0'][:,:] # Read in reverse direction
levs = f.variables['lv_ISBL0'][:]

levelindex = np.ravel(levs==level2plot[0])

temp_full = f.variables['TMP_P0_L100_GLC0'][:,:,:]
u_full = f.variables['UGRD_P0_L100_GLC0'][:,:,:]
v_full = f.variables['VGRD_P0_L100_GLC0'][:,:,:]
f.close

pres = np.zeros_like(temp_full).astype('f')   
for kk in range(0,len(levs)):      
   pres[kk,:,:] = levs[kk]


theta_full = wm.temp_to_theta(temp_full, pres)

dtdp,dtdy,dtdx = wm.gradient_cartesian(temp_full, levs, deltax, deltax)
dthdp,dthdy,dthdx = wm.gradient_cartesian(theta_full, levs, deltax, deltax)

avort_lev = wm.vertical_vorticity_cartesian(u_full[levelindex,:,:].squeeze(), v_full[levelindex,:,:].squeeze(), lats, deltax, deltax, 1)

epv = wm.epv_cartesian(theta_full,levs,u_full,v_full,lats,deltax,deltax)
epv_lev = epv[levelindex,:,:].squeeze()


# Squeeze and convert to degrees Celsius
tempplot = temp_full[levelindex,:,:].squeeze() - 273.15
gradx_lev = dthdx[levelindex,:,:].squeeze()
grady_lev = dthdy[levelindex,:,:].squeeze()
gradz_lev = dthdp[levelindex,:,:].squeeze()


base_cntr_hgrad = 0
cint_hgrad = 4*10**-6   
cbar_min_hgrad = base_cntr_hgrad-14*cint_hgrad
cbar_max_hgrad = base_cntr_hgrad+14*cint_hgrad
cbar_max_hgrad = cbar_max_hgrad + (cint_hgrad/2)   
   
base_cntr_vgrad = 0
cint_vgrad = 5*10**-5   
cbar_min_vgrad = base_cntr_vgrad-14*cint_vgrad
cbar_max_vgrad = base_cntr_vgrad+14*cint_vgrad
cbar_max_vgrad = cbar_max_vgrad + (cint_vgrad/2)   

base_cntr_avort = 1*10**-4  
cint_avort = 1*10**-5   
cbar_min_avort = base_cntr_avort-14*cint_avort
cbar_max_avort = base_cntr_avort+14*cint_avort
cbar_max_avort = cbar_max_avort + (cint_avort/2)   


cflevs =  np.arange(-30,31,1)
cflevs_hgrad = np.arange(cbar_min_hgrad, cbar_max_hgrad, cint_hgrad)
cflevs_vgrad = np.arange(cbar_min_vgrad, cbar_max_vgrad, cint_vgrad)
cflevs_avort = np.arange(cbar_min_avort, cbar_max_avort, cint_avort)
cflevs_epv = np.arange(0, 6, 0.1)

golden = (np.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 16./golden), dpi=128)

ny,nx = np.shape(lons)

urlat = lats[ny-1,nx-1]
lllat = lats[0,0]
lllon = lons[0,0]
urlon = lons[ny-1,nx-1]


fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
m = Basemap(resolution='i', projection='lcc', llcrnrlon=lllon,
    llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, lat_1=35.0, lon_0=-98.2,
    lat_2=35.0, rsphere=(6378137.00, 6356752.3142), area_thresh=10000)    

m.drawcoastlines(linewidth=2, color='#444444', zorder=6)
m.drawcountries(linewidth=1, color='#444444', zorder=5)
m.drawstates(linewidth=0.66, color='#444444', zorder=4)
m.drawmapboundary

# draw lat/lon grid lines every 30 degrees.
m.drawmeridians(np.arange(0, 360, 30))
m.drawparallels(np.arange(-90, 90, 30))

new_lons, new_lats = m(lons, lats)

CS1 = m.contourf(new_lons,new_lats,tempplot,cmap=plt.cm.jet,levels=cflevs, extend='both',zorder=1)
cbar = plt.colorbar(CS1, shrink=0.95, orientation='horizontal',extend='both')

fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
m = Basemap(resolution='i', projection='lcc', llcrnrlon=lllon,
    llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, lat_1=35.0, lon_0=-98.2,
    lat_2=35.0, rsphere=(6378137.00, 6356752.3142), area_thresh=10000)    


m.drawcoastlines(linewidth=2, color='#444444', zorder=6)
m.drawcountries(linewidth=1, color='#444444', zorder=5)
m.drawstates(linewidth=0.66, color='#444444', zorder=4)
m.drawmapboundary

# draw lat/lon grid lines every 30 degrees.
m.drawmeridians(np.arange(0, 360, 30))
m.drawparallels(np.arange(-90, 90, 30))


CS1 = m.contourf(new_lons,new_lats,avort_lev,cmap=plt.cm.jet,levels=cflevs_avort, extend='both',zorder=1)
cbar = plt.colorbar(CS1, shrink=0.95, orientation='horizontal',extend='both')


fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
m = Basemap(resolution='i', projection='lcc', llcrnrlon=lllon,
    llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, lat_1=35.0, lon_0=-98.2,
    lat_2=35.0, rsphere=(6378137.00, 6356752.3142), area_thresh=10000)    


m.drawcoastlines(linewidth=2, color='#444444', zorder=6)
m.drawcountries(linewidth=1, color='#444444', zorder=5)
m.drawstates(linewidth=0.66, color='#444444', zorder=4)
m.drawmapboundary

# draw lat/lon grid lines every 30 degrees.
m.drawmeridians(np.arange(0, 360, 30))
m.drawparallels(np.arange(-90, 90, 30))


CS1 = m.contourf(new_lons,new_lats,grady_lev,cmap=plt.cm.jet,levels=cflevs_hgrad, extend='both',zorder=1)
cbar = plt.colorbar(CS1, shrink=0.95, orientation='horizontal',extend='both')


fig = plt.figure(figsize=(8., 16./golden), dpi=128)   # New figure
m = Basemap(resolution='i', projection='lcc', llcrnrlon=lllon,
    llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, lat_1=35.0, lon_0=-98.2,
    lat_2=35.0, rsphere=(6378137.00, 6356752.3142), area_thresh=10000)    


m.drawcoastlines(linewidth=2, color='#444444', zorder=6)
m.drawcountries(linewidth=1, color='#444444', zorder=5)
m.drawstates(linewidth=0.66, color='#444444', zorder=4)
m.drawmapboundary

# draw lat/lon grid lines every 30 degrees.
m.drawmeridians(np.arange(0, 360, 30))
m.drawparallels(np.arange(-90, 90, 30))


CS1 = m.contourf(new_lons,new_lats,gradz_lev,cmap=plt.cm.jet,levels=cflevs_vgrad, extend='both',zorder=1)
cbar = plt.colorbar(CS1, shrink=0.95, orientation='horizontal',extend='both')



plt.show()

