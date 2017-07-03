#!/usr/bin/python

import numpy as np
#import matplotlib.pyplot as mpl
import matplotlib as plt
from mpl_toolkits.basemap import Basemap, addcyclic 

def nan2zero(data):
    ''' Convert NaNs to zero '''
    ''' '''
    ''' data: Input data array '''
    dimens = np.shape(data)
               
    # Temporarily collapse data array
    temp = np.reshape(data,np.prod(np.size(data)), 1)       
    
    # Find indices with NaNs
    inds = np.argwhere(np.isnan(temp))    
    
    # Replace NaNs with zero
    temp[inds] = 0.                 
    
    # Turn vector back into array
    data = np.reshape(temp,dimens,order='F').copy()
 
    return data

def zero2nan(data):
    ''' Convert zeros to Nans '''
    ''' '''
    ''' data: Input data array '''
    dimens = np.shape(data)
               
    # Temporarily collapse data array
    temp = np.reshape(data,np.prod(np.size(data)), 1)       
    
    # Find indices with NaNs
    inds = np.argwhere(temp==0)    
    
    # Replace zeros with NaNs
    temp[inds] = float('NaN')                 
    
    # Turn vector back into array
    data = np.reshape(temp,dimens,order='F').copy()
 
    return data

def filter_numeric_nans(data,thresh,repl_val,high_or_low) :
    ''' Filter numerical nans above or below a specified value'''
    ''' '''
    ''' data:        (Input) array to filter '''
    ''' thresh:      (Input) threshold value to filter above or below '''
    ''' repl_val:    (Input) replacement value'''
    ''' high_or_low: (Input)''' 


    dimens = np.shape(data);
    temp = np.reshape(data,np.prod(np.size(data)), 1)
    if high_or_low=='high':        	
	inds = np.argwhere(temp>thresh) 	
	temp[inds] = repl_val	  
    elif high_or_low=='low':    
        inds = np.argwhere(temp<thresh) 
	temp[inds] = repl_val	  
    elif high_or_low =='both':
       	inds = np.argwhere(temp>thresh) 	
	temp[inds] = repl_val
	del inds
       	inds = np.argwhere(temp<-thresh) 	
	temp[inds] = -repl_val	                 
    else:
        inds = np.argwhere(temp>thresh) 
	temp[inds] = repl_val	  

    # Turn vector back into array
    data = np.reshape(temp,dimens,order='F').copy()
 
    return data    
    
def bold_labels(ax,fontsize=None):
    if fontsize is None:
        fontsize = 14
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')

#def draw_map_background(m, ax=mpl.gca()):
#    ''' Setup the map background '''
#    m.drawcoastlines(ax=ax, linewidth=2, color='#444444', zorder=6)
#    m.drawcountries(ax=ax, linewidth=1, color='#444444', zorder=5)
#    m.drawstates(ax=ax, linewidth=0.66, color='#444444', zorder=4)
#    m.drawmapboundary
    
def lonswap(d,subtract=0.):
        sh = np.shape(d)	
	midl = sh[1]/2	
	midl = np.round(midl)
	h=d[:,midl:].copy()-subtract
	d[:,midl:]=d[:,:midl].copy()
	d[:,:midl]=h
	return d
	    
def periodic(d,add=0.):
	return np.append( d, (d[:,0].copy()+add).reshape(-1,1) , 1)    
	
def advance_time(timestrin,timeinc):
    ''' Advances or reverses a time by timeinc'''
    ''' '''
    ''' timestrin: (Input) time string in yyyymmddhh format'''
    ''' timeinc:   (Input) number of hours to increment or decrement'''
    '''             Use a negative sign to decrement '''
    
    import datetime
        
    yyyy = timestrin[0:4]
    mm = timestrin[4:6]
    dd = timestrin[6:8]
    hh = timestrin[8:10]	
	
    date=datetime.datetime(int(yyyy),int(mm),int(dd),int(hh))
    date += datetime.timedelta(hours=timeinc)
    tt = date.timetuple()
    
    yyyy = str(tt[0])
    mm = str(tt[1])
    dd = str(tt[2])
    hh = str(tt[3])
    
    if tt[0]<1000: yy = '0'+mm 
    if tt[1]<10: mm = '0'+mm 
    if tt[2]<10: dd = '0'+dd
    if tt[3]<10: hh = '0'+hh
    
    timestrin = yyyy+mm+dd+hh        
    
    return timestrin
def get_cmap_cust():
    ''' Setup a custom colortable. '''
    cdict = {'red': ((0.00, 240/255., 220/255.),
                         (0.25, 40/255., 20/255.),
                         (0.50, 225/255., 255/255.),
                         (0.75, 150/255., 150/255.),
                         (1.00, 255/255., 255/255.)),

             'green': ((0.00, 240/255., 220/255.),
                         (0.25, 0/255., 50/255.),
                         (0.50, 255/255., 255/255.),
                         (0.75, 0/255., 35/255.),
                         (1.00, 225/255., 240/255.)),

             'blue': ((0.00, 255/255., 255/255.),
                         (0.25, 160/255., 150/255.),
                         (0.50, 255/255., 170/255.),
                         (0.75, 0/255., 35/255.),
                         (1.00, 225/255., 240/255.))}
    return plt.colors.LinearSegmentedColormap('cool2warm', cdict, 256)
def cmap_discretize(cmap, N):
   """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: Number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
       imshow(x, cmap=djet)
   """
   from scipy import interpolate
   
   cdict = cmap._segmentdata.copy()
   # N colors
   colors_i = np.linspace(0,1.,N)
   # N+1 indices
   indices = np.linspace(0,1.,N+1)
   for key in ('red','green','blue'):
       # Find the N colors
       D = np.array(cdict[key])
       I = interpolate.interp1d(D[:,0], D[:,1])
       colors = I(colors_i)
       # Place these colors at the correct indices.
       A = np.zeros((N+1,3), float)
       A[:,0] = indices
       A[1:,1] = colors
       A[:-1,2] = colors
       # Create a tuple for the dictionary.
       L = []
       for l in A:
           L.append(tuple(l))
       cdict[key] = tuple(L)
   # Return colormap object.
   return plt.colors.LinearSegmentedColormap('colormap',cdict,1024)

def cmap_whitezero(cmap,N,Nwhites,pos):
   """Whites out middle index of a colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: Number of colors.
	Nwhites: Number of whites
	pos: Position for white bar; if -1, will place in middle
	                             if  0, will place at bottom

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
       imshow(x, cmap=djet)
   """
   from scipy import interpolate
   
   if ( pos == -1 ):
      mid = np.round(N/2)
      mid = int(mid)
   else:
      mid = pos
   
   nadd = Nwhites - 1
   
   
   cdict = cmap._segmentdata.copy()
   # N colors
   colors_i = np.linspace(0,1.,N)

   # N+1 indices
   indices = np.linspace(0,1.,N+1)
   for key in ('red','green','blue'):
       # Find the N colors
       D = np.array(cdict[key])
       I = interpolate.interp1d(D[:,0], D[:,1])
       colors = I(colors_i)
       colors[mid] = 1.
       isodd = 0
       if ( np.mod(N,2) == 0 ) :           
	  colors[mid-1] = 1.
	  isodd = 1
       kk=mid-nadd
       kend=mid+nadd 
       if ( kk < kend ) :      
          while (kk <= kend) :
             colors[kk] = 1.
             kk += 1
       if (isodd == 1 ): colors[kk] = 1.   	  
       # Place these colors at the correct indices.
       A = np.zeros((N+1,3), float)
       A[:,0] = indices
       A[1:,1] = colors
       A[:-1,2] = colors       
       # Create a tuple for the dictionary.
       L = []
       for l in A:
           L.append(tuple(l))
       cdict[key] = tuple(L)
   # Return colormap object.
   return plt.colors.LinearSegmentedColormap('colormap',cdict,1024)

def earth_distm(lat1,lon1,lat2,lon2):
    """

   Calculates the distances between a point and all other points given a latitude and longitude

   Input:    
       lat1, lon1 - Coordinate pair to calculate distance from (must be single values)
       lat2, lon2 - Coordinates to calculate distance to (can be vector or array)
   Output:
       ed - distance between pairs in km
       
    Steven Cavallo
    February 2013
    University of Oklahoma
    
    """
    
    latshape = np.shape(lat2)
    latsize = np.size(lat2)
    
    R_earth = 6371200
    R_earth = R_earth / 1000
    pid = np.pi/180

    if latsize > 1:
       [iy,ix] = np.shape(lat2)
       
       X = np.zeros_like(lat2).astype('f')   
       Y = np.zeros_like(lon2).astype('f')   
       for ii in range(0,ix):
           for jj in range(0,iy):   
               X[jj,ii] = lon1
	       Y[jj,ii] = lat1      
    else:
       X = lon1
       Y = lat1   
    	            
    # calculate distance
    ed = R_earth * np.arccos( np.sin(Y*pid) * np.sin(lat2*pid) + np.cos(Y*pid) * np.cos(lat2*pid) * np.cos((lon2 - X)*pid));

    return ed

def destagger_hor_wind(ustag,vstag):
   """
   u,v = destagger_hor_wind(ustag,vstag)

   destaggers horizontal wind

   Steven Cavallo
   March 2013

   """
   
   nshape = np.shape(ustag)
   nel = len(nshape)   
   if nel == 2:
      Ny,Nx = np.shape(ustag)         
      
      u = np.zeros((Ny,Nx-1))
      v = np.zeros((Ny,Nx-1))
      
      for jj in range(0,Ny):
         for ii in range(0,Nx-1):	 	     
             u[jj,ii] = (ustag[jj,ii+1] + ustag[jj,ii])/2


      for jj in range(0,Ny):
         for ii in range(0,Nx-1):			
             v[jj,ii] = (vstag[jj+1,ii] + ustag[jj,ii])/2   
   
   else:
      Nz,Ny,Nx = np.shape(ustag)   
       
      u = np.zeros((Nz,Ny,Nx-1))
      v = np.zeros((Nz,Ny,Nx-1))
      for kk in range(0,Nz):
	 for jj in range(0,Ny):
            for ii in range(0,Nx-1):	 		
        	u[kk,jj,ii] = (ustag[kk,jj,ii+1] + ustag[kk,jj,ii])/2

      for kk in range(0,Nz):
	 for jj in range(0,Ny):
            for ii in range(0,Nx-1):			
        	v[kk,jj,ii] = (vstag[kk,jj+1,ii] + ustag[kk,jj,ii])/2   

   return u,v
def grid_to_true_wind(lon,ug,vg,truelat1,truelat2,stdlon,proj_type):
    """

   converts from grid relative wind to true direction wind.  Based on FSL 
   mapping module.

   Input:    
       lon - 2D longitude array on grid wind points
       ug, vg - 2D arrays of grid u and v winds
       truelat1,truelat2 - true latitudes
       stdlon - standard longitude
       proj_type - projection type
   Output:
       ut,vt - output u and v true winds
       
    Steven Cavallo
    March 2013
    University of Oklahoma
    
    """
        
    
    Ny,Nx = np.shape(ug)         
      
    ut = np.zeros((Ny,Nx))
    vt = np.zeros((Ny,Nx))    
    
    pid = np.pi/180
    
    if proj_type == 'lambert':
       cone = (np.log(np.cos(truelat1*pid))-np.log(np.cos(truelat2*pid))) / (np.log(np.tan((90. - abs(truelat1)) * pid * 0.5 )) - \
            np.log(np.tan((90. - abs(truelat2)) * pid * 0.5 )) )           
    if proj_type == 'polar':
       cone = 1
       
    if ( (proj_type == 'polar') or (proj_type == 'lambert') ):
       diff = lon - stdlon
       Ny,Nx = np.shape(diff)       
       for jj in range(0,Ny):
          for ii in range(0,Nx):	 	     
	      diffnow = lon[jj,ii] - stdlon
	      if diffnow > 180:
                 diffnow = diffnow - 360
	      if diffnow < -180:
                 diffnow = diffnow + 360                 
       
	      alpha = diffnow * cone * pid * 1 * np.sign(truelat1); 
	      ut[jj,ii] = vg[jj,ii] * np.sin(alpha) + ug[jj,ii] * np.cos(alpha);
	      vt[jj,ii] = vg[jj,ii] * np.cos(alpha) - ug[jj,ii] * np.sin(alpha);    
    
    else:
       ut = ug
       vt = vg

    return ut,vt

def xsection_inds(slon, slat, elon, elat, lons, lats, m):
    '''
    Returns the indicies for creating a cross section.
    Note: The indices returned are generall south-to-north

    Parameters
    ----------
    slon : scalar
        The longitude value of the starting point
    slat : scalar
        The latitude value of the starting point
    elon : scalar
        The longitude value of the ending point
    elat : scalar
        The latitude value of the ending point
    lons : 2D array_like
        The longitude values of the underlying dataset
    lats : 2D array_like
        The latitude values of the underlying dataset
    m : Basemap Instance
        The basemap instance used for plotting data on a map

    Returns
    -------
    xinds : numpy array
        The first dimension indices of the cross section
    yinds : numpy array
        The second dimension indices of the cross section

    '''
    
    import scipy.spatial as ss
    from PIL import Image, ImageDraw
    
    x, y = m(lons, lats)
    gpoints = zip(x.ravel(), y.ravel())
    gtree = ss.cKDTree(gpoints)
    sx, sy = m(slon, slat)
    ex, ey = m(elon, elat)
    pts = np.array([(sx, sy), (ex, ey)])
    dists, inds = gtree.query(pts, k=1, distance_upper_bound=100*1000.)
    xinds, yinds = np.unravel_index(inds, x.shape)
    pts = ((yinds[0], xinds[0]), (yinds[1], xinds[1]))
    grid = np.zeros_like(lons)
    img = Image.new('L', grid.shape[::-1], 0)
    ImageDraw.Draw(img).line(pts, fill=1, width=1)
    img = np.array(img)
    xinds, yinds = np.where(img > 0)
    if slat > elat:
        xinds = xinds[::-1]
        yinds = yinds[::-1]
    return xinds, yinds
