import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import sys
import pandas as pd
from datetime import datetime
from mpl_toolkits.basemap import Basemap
import numpy.ma as ma
from mpl_toolkits.axes_grid1 import make_axes_locatable




"""
# read in the netcdf file, file given as argument in the command line	
filename = sys.argv[1]	
dataset = nc.Dataset(filename)
BT_band10_masked = np.array(dataset.variables['BT10_masked'])
BT_band11_masked = np.array(dataset.variables['BT11_masked'])

BT_band10_masked = np.ma.masked_where(BT_band10_masked > 350, BT_band10_masked)
BT_band11_masked = np.ma.masked_where(BT_band11_masked > 350, BT_band11_masked)

BT_band10_mean = np.mean(BT_band10_masked)
BT_band10_max = np.amax(BT_band10_masked)

BT_band11_mean = np.mean(BT_band11_masked)
BT_band11_max = np.amax(BT_band11_masked)
"""
#print BT_band11_mean
#print BT_band11_max

"""
#Dungeness
BT_band10_mean = [279.895240398 , 285.257169811 , 288.845133403 , 287.034093396 , 290.716541463 , 289.441273791 , 280.280683538 , 282.284029787 , 281.057314834 , 278.405306139 , 281.483158499 , 289.141392084 , 289.886755506 , 282.52736908 , 286.852355537 , 282.361197765 , 289.066462689 , 281.320482392 , 282.65342557 , 282.944857456 , 287.299189931 , 286.917271161 , 290.391612983]
BT_band10_max = [281.351 , 294.95 , 299.022 , 291.241 , 302.65 , 297.921 , 282.431 , 289.464 , 283.38 , 280.04 , 287.065 , 295.764 , 294.668 , 283.888 , 295.104 , 289.189 , 296.599 , 287.044 , 283.882 , 290.897 , 295.458 , 295.075 , 296.459]
BT_band11_mean = [278.537493092 , 284.215437393 , 288.196733098 , 285.451897238 , 290.405245631 , 287.973943619 , 279.438263349 , 281.86952361 , 279.878062557 , 277.512680565 , 281.049215907 , 287.651899462 , 288.508222573 , 281.729119753 , 285.85874474 , 281.937342564 , 288.106748258 , 280.902666169 , 281.847358195 , 282.303688544 , 286.741413939 , 285.909774619 , 288.850601124]
BT_band11_max = [279.8 , 293.048 , 297.013 , 289.382 , 300.197 , 294.777 , 281.804 , 288.991 , 281.985 , 279.202 , 286.052 , 292.665 , 292.711 , 283.081 , 292.435 , 288.874 , 294.516 , 286.945 , 283.069 , 289.876 , 293.971 , 292.406 , 293.579]

#Heysham
BT_band10_mean = [280.761785154 , 287.77732629 , 286.98519591 , 284.346593904 , 286.807492331 , 286.380418762 , 289.961238965]
BT_band10_max = [287.848 , 297.443 ,292.621 , 292.693 , 294.169 , 292.118 , 295.143]
BT_band11_mean = [279.417201886 , 286.445874948 , 284.958990137 , 283.473453358 , 285.109774403 , 285.194899988 , 288.404962801]
BT_band11_max = [285.785 , 293.934 , 289.564 , 290.828 , 291.383 , 289.733 , 292.636]

#Hartlepool
BT_band10_mean = [286.345195163 , 286.493289256]
BT_band10_max = [295.706 , 297.424]
BT_band11_mean = [285.719905923 , 285.974223706]
BT_band11_max = [293.282, 294.86]

#Hinkley
BT_band10_mean = [283.809269774 , 277.574840621 , 290.685629997 , 283.53417442 , 287.191126365 , 278.584367924 , 290.23506116 , 287.834435617]
BT_band10_max = [289.598 , 285.059 , 297.548 , 288.026 , 291.909 , 286.504 , 296.031 , 294.383]
BT_band11_mean = [282.445899908 , 276.428302056 , 289.2592903 , 283.002119717 , 286.33841562 , 278.116980985 , 289.207886865 , 286.917596107]
BT_band11_max = [287.509 , 283.134 , 294.797 , 287.464 , 290.228 , 285.613 , 294.339 , 292.662]

#Sizewell
BT_band10_mean = [284.117150681 , 279.107700245 , 277.767050901 , 289.229945148 , 281.897272504 , 280.110662987 , 291.099341325 , 287.618174179 , 279.227091066 , 281.328835119 , 276.825168939 , 281.243708754 , 289.090783019 , 286.466926891 , 279.226348784 , 281.33103731 , 271.594269249 , 276.826243865 , 281.242094107 , 289.087508544 , 290.286705857 , 278.617381875 , 286.801339782]
BT_band10_max = [287.007 , 281.965 , 279.995 , 300.186 , 283.92 , 287.592 , 304.757 , 298.128 , 281.639 , 288.926 , 281.932 , 287.427 , 296.179 , 299.565 , 281.578 , 289.289 , 278.785 , 281.935 , 287.393 , 296.305 , 294.68 , 280.601 , 292.296]
BT_band11_mean = [282.551318063 , 278.044885851 , 276.717723106 , 288.087739611 , 280.67602675 , 278.979740088 , 290.117598713 , 285.873933137 , 278.334309738 , 280.79883594 , 275.805305053 , 280.63110598 , 287.604247304 , 285.84569399 , 278.333966565 , 280.802202308 , 271.210084841 , 275.806755846 , 280.630351771 , 287.602410886 , 288.940623746 , 277.62351648 , 285.571492106]
BT_band11_max = [285.17 , 280.606 , 278.564 , 298.581 , 282.455 , 285.788 , 301.112 , 294.888 , 280.753 , 287.379 , 280.481 , 286.464 , 293.735 , 296.816 , 280.696 , 288.452 , 278.045 , 280.484 , 286.418 , 293.801 , 293.068 , 279.532 , 289.65]

#Torness
BT_band10_mean = [285.034680841 , 279.423963536 , 285.549098736 , 285.565205766 , 277.601922251 , 283.441523201 , 281.10762055]
BT_band10_max = [296.802 , 284.164 , 290.904 , 292.703 , 284.436 , 288.436 , 286.39]
BT_band11_mean = [284.010821376 , 278.0140885 , 285.206325812 , 285.073458276 , 276.988566321 , 282.387458671 , 280.717950477]
BT_band11_max = [294.505 , 281.918 , 289.793 , 291.366 , 283.482 , 286.893 , 285.619]
"""

BT_band10_mean = np.array(BT_band10_mean)
BT_band10_max = np.array(BT_band10_max)
BT_band11_mean = np.array(BT_band11_mean)
BT_band10_max = np.array(BT_band10_max)


plt.subplot(211)
bins = np.linspace(273, 305, 10)
plt.hist(BT_band10_mean, bins, alpha=0.5, label='BT_band10_mean')
plt.hist(BT_band10_max, bins, alpha=0.5, label='BT_band10_max')
plt.legend(loc='upper right')
plt.subplot(212)
bins = np.linspace(273, 305, 10)
plt.hist(BT_band11_mean, bins, alpha=0.5, label='BT_band11_mean')
plt.hist(BT_band11_max, bins, alpha=0.5, label='BT_band11_max')
plt.legend(loc='upper right')
plt.suptitle('Histogram of BT for Torness averaged over all clear sky scenes' , fontsize=14)
plt.show()

plt.subplot(211)
bins = np.linspace(0, 15, 20)
plt.hist(BT_band10_max - BT_band10_mean, bins, alpha=0.5, label='BT10_max - BT10_mean')
plt.legend(loc='upper right')
plt.subplot(212)
bins = np.linspace(0, 15, 20)
plt.hist(BT_band11_max - BT_band11_mean, bins, alpha=0.5, label='BT11_max - BT11_mean')
plt.legend(loc='upper right')
plt.suptitle('Histogram of BT max - BT mean for Torness averaged over all clear sky scenes' , fontsize=14)
plt.show()
