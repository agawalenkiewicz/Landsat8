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
	sum = result_array.sum(axis=0)
	sumPercentail = np.percentile(sum, 95.)
	print sumPercentail
	sum[sum >= sumPercentail] = 10
	sum[sum < 10] = 0
	sum[sum > 0] = 1
	plt.imshow(sum)
	plt.title('Dungeness landmask')
	plt.show()
	# Apply the mask from band 11 to remove black pixels from the image.
	sum = np.ma.masked_where(sum == 1, sum)
	Landmask = np.ma.getmaskarray(sum)
	return Landmask

def plot_stat_mask(filepath, Landmask):
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



#in_lat = sys.argv[1]
#in_lon = sys.argv[2]
#out_lat = sys.argv[3]
#out_lon = sys.argv[4]
inflow_temp_b10 = []
inflow_temp_b11 = []
outflow_temp_b10 = []
outflow_temp_b11 = []

"""
for element in filename:
	element_path = os.path.join('/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/dungeness_checked', element)
	nc_file = nc.Dataset(element_path)
	print nc_file.variables.keys()
	lats = nc_file.variables['latitude'][:,0]
	lons = nc_file.variables['longitude'][0,:]

	in_lat_idx = geo_idx(in_lat, lats)
	in_lon_idx = geo_idx(in_lon, lons)
	out_lat_idx = geo_idx(out_lat, lats)
	out_lon_idx = geo_idx(out_lon, lons)

	#print "in_lat_idx" , in_lat_idx
	#print "in_lon_idx" , in_lon_idx
	
	#print "out_lat_idx" , out_lat_idx
	#print "out_lon_idx" , out_lon_idx
	
	inflow_temp_b10.append(nc_file.variables['BT_band10'][in_lat_idx,in_lon_idx])
	inflow_temp_b11.append(nc_file.variables['BT_band11'][in_lat_idx,in_lon_idx])
	outflow_temp_b10.append(nc_file.variables['BT_band10'][out_lat_idx,out_lon_idx])
	outflow_temp_b11.append(nc_file.variables['BT_band11'][out_lat_idx,out_lon_idx])
	aga_outflow_b10.append(nc_file.variables['BT_band11'][232,231])
	aga_outflow_b11.append(nc_file.variables['BT_band11'][232,231])

	#print "inflow_temp_b10" , inflow_temp_b10
	#print "inflow_temp_b11" , inflow_temp_b11
	#print "outflow_temp_b10" , outflow_temp_b10
	#print "outflow_temp_b11" , outflow_temp_b11
	

with open('dungeness_inflow_temp_b10', 'wb') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(inflow_temp_b10)
with open('dungeness_inflow_temp_b11', 'wb') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(inflow_temp_b11)
with open('dungeness_outflow_temp_b10', 'wb') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(outflow_temp_b10)
with open('dungeness_outflow_temp_b11', 'wb') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(outflow_temp_b11)

with open('dungeness_outflow_temp_aga_b10', 'wb') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(aga_outflow_b10)
with open('dungeness_outflow_temp_aga_b11', 'wb') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(aga_outflow_b11)
"""