from osgeo import gdal
import os
import steps as s
import numpy as np

the_folder = '/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/heysham/LC82040222015161LGN01/scenes/' 

# dFilenames[i] = "LC82040212013155LGN00_B{}_crop.TIF".format(i)
Filename = "LC08_L1TP_204022_20150610_20170408_01_T1_B10.TIF"  
	
the_metafile = 'LC08_L1TP_204022_20150610_20170408_01_T1_MTL.txt'
metadata = s.get_metadata(the_folder, the_metafile)
 
lines = np.int(metadata['THERMAL_LINES'])
samples = np.int(metadata['THERMAL_SAMPLES'])

# Open tif file
ds = gdal.Open('/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/heysham/LC82040222015161LGN01/scenes/LC08_L1TP_204022_20150610_20170408_01_T1_B10.TIF', gdal.GA_ReadOnly)
# GDAL affine transform parameters, According to gdal documentation xoff/yoff are image left corner, a/e are pixel wight/height and b/d is rotation and is zero if image is north up. 
xoff, a, b, yoff, d, e = ds.GetGeoTransform()


# get columns and rows of your image from gdalinfo
rows = lines
colms = samples
pixel_coord = np.zeros([])

def pixel2coord(x, y):

    #Returns global coordinates from pixel x, y coords
	xp = a * x + b * y + xoff
	yp = d * x + e * y + yoff
	"""
	lat_num = []
	lon_num = []
	for row in  range(0,rows):
		for col in  range(0,colms): 
			lat_num.append(xp)
			lon_num.append(yp)
	"""		
	return(xp, yp)