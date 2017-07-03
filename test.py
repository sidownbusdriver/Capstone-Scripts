#mports
import netCDF4

import os, datetime
import numpy as np
import matplotlib as mpl
from scipy import ndimage
import matplotlib.cm as cm

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid

# Add a couple of user defined functions
import weather_modules as wm
import utilities_modules as um

# Test Figure
import netCDF4 as nc
f = nc.Dataset('/archive/capstone/sea_ice/wrfout_d01_1975-12-01_00:00:00', "r")

# Read in variables
ice = f.variables['SEAICE'][:]
lat = f.variables['XLAT'][:]
lon = f.variables['XLONG'][:]

ice=ice[0]
lat=lat[0]
lon=lon[0]
#print ice

# Map
m = Basemap(projection='npstere',boundinglat=40,lon_0=270,resolution='l')

# Set map properties
golden = (np.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 16./golden), dpi=128)

# Making figure
fig = plt.figure(figsize=(8., 16./golden), dpi=128) # New figure
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Convert lat and lon
new_lon, new_lat = m(lon, lat)

# Plotting
#plt.contour(new_lon, new_lat, ice, 1, colors='grey', linewidths=85.0, linestyle='solid', zorder=1)
plt.contourf(new_lon, new_lat, ice, 1)

m.drawcoastlines()
m.fillcontinents(color='white',lake_color='DodgerBlue', zorder=2)
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,10.))
m.drawmeridians(np.arange(-180.,181.,10.))
m.drawmapboundary(fill_color='DodgerBlue')

plt.title("North Polar Stereographic Projection")
plt.savefig('test.png', bbox_inches='tight')
plt.show()
