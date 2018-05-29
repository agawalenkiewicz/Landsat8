import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os

import Landsat_ncfiles



def geo_idx(dd, dd_array):
   """
     search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
    """
   geo_idx = (np.abs(dd_array - np.float(dd))).argmin()
   return geo_idx

def stack_water_detection(filename, path):
	"""
	Input:
	filename - list of netcdf files with MNDWI mask
	path - absolute path to where the netcdf files are stored
	---
	loops through all files in the given list, finds the MNDWI masked layer
	for each layer gives value of 1 if land, 0 is water
	stacks the masks together as a 3D array
	---
	Output: 3D array of 0-1 masks
	"""
	result_array = np.zeros((len(filename), 401, 401))
	for i, element in enumerate(filename):
		element_path = os.path.join(path, element)
		nc_file = nc.Dataset(element_path)
		#print nc_file.variables.keys()
		BT_masked = np.array(nc_file.variables['BT10_masked'])
		BT_masked[BT_masked > 350] = 1
		BT_masked[BT_masked > 1] = 0
		result_array[i,:,:] = BT_masked
	#plt.imshow(BT_masked)
	#plt.show()
	print np.shape(result_array)
	return result_array
	
def stat_landmask(result_array):
	"""
	Input: 3D arrat of 0-1 masks
	---
	sums the value of each pixel in the vertical (through all stacked layers)
	created a 2D layer with summed pixel values
	to normalize the output, it calculates the 95th percentile from the sum
	95th percentile is now the threshols value
	where pixel value above thershold - land
	where pixel values below threshold - water
	masks all pixels that were treated as land
	---
	Output: landmask based on 95th percentile of summed pixel values
	"""
	sum = result_array.sum(axis=0)
	sumPercentail = np.percentile(sum, 95.)
	print sumPercentail
	sum[sum >= sumPercentail] = 10
	sum[sum < 10] = 0
	sum[sum > 0] = 1
	plt.imshow(sum)
	plt.title('Dungeness landmask')
	plt.show()
	# Apply the mask to remove land pixels from the image.
	sum = np.ma.masked_where(sum == 1, sum)
	Landmask = np.ma.getmaskarray(sum)
	return Landmask

def plot_stat_mask(filepath, Landmask):
	"""
	Input: path to netcdf file we want to process, 95th percentile landmask
	----
	choose the variable from the netcdf file (SST, BT)
	apply a landmask over the chosen variable
	plot a 2D image with the landmask active
	---
	Output: shwoing the 2D masked plot
	"""
	data_path = filepath
	data = nc.Dataset(data_path)
	#choose BT at 10.8 micron
	variable = np.array(data.variables['BT_band10'])
	variable = np.ma.array(variable, mask=Landmask)
	plt.imshow(variable)
	plt.show()

# if you want different place, change it after the dot
filename = Landsat_ncfiles.dungeness
path = Landsat_ncfiles.dungeness_path

masked_stack = stack_water_detection(filename, path)
landmask = stat_landmask(masked_stack)
#exampleFilePath = os.path.join(path, filename[-1])
exampleFilePath = '/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/dungeness_checked/LC82000252014034LGN01/scenes/LC08_L1TP_200025_20140203_20170426_01_T1.nc'
plot_stat_mask(exampleFilePath, landmask)