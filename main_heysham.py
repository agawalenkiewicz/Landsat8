# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 14:28:33 2017

@author: Agnieszka
"""
import steps as s
import proj_grid as p
import regridding as r
import convert_netcdf as conv_nc

import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt

import pdb

def main(band1, band2, band3, band4, band5, band6, band7, band8, band9, band10, band11):

    #the_folder = 'E:/PHD/datastore/EE/LANDSAT_8_C1/hinckley/LC82030242013308LGN01/scenes/'
	the_folder = sys.argv[1] #'/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/dungeness_checked/LC82010252015108LGN01/scenes/' 
    # Dictionary of the unique filenames for the bands needed.
	dFilenames = {}
	for i in [band1, band2, band3, band4, band5, band6, band7, band8, band9, band10, band11]:
		# dFilenames[i] = "LC82040212013155LGN00_B{}_crop.TIF".format(i)
		dFilenames[i] = sys.argv[2].format(i) #"LC08_L1TP_201025_20150418_20170409_01_T1_B{}.TIF".format(i)    
	
	the_metafile = sys.argv[3] #'LC08_L1TP_201025_20150418_20170409_01_T1_MTL.txt'
	metadata = s.get_metadata(the_folder, the_metafile) 
    
    #p = re.compile(r'(?<=_B)[^.]+')
    #for fn in os.listdir(the_folder):
    #    try: 
    #    	file_name = fn
    #    	file_band = p.search(fn).group(0)
    #    except AttributeError:
    #        if fn.endswith('MTL.txt'):
    #            the_metafile = fn

	x_origin, y_origin, read_info_old_coord_sys, dataset = s.read_info(the_folder, dFilenames[band10])
	print(dataset)
	print(x_origin)
	print(y_origin)
	
	lat_im, lon_im = s.latlon_image(the_folder, dFilenames[band10])
	print(np.amin(lat_im))
	print(np.amax(lat_im))
	print(np.amin(lon_im))
	print(np.amax(lon_im))
	print("lat_im", lat_im.shape)
	print("lon_im", lon_im.shape)
	print(lat_im)
	print(lon_im)
	
	lines = np.int(metadata['THERMAL_LINES'])
	samples = np.int(metadata['THERMAL_SAMPLES'])

	
	# Dictionary of band data.
	data = {}
    #for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
	for i in [band1, band2, band3, band4, band5, band6, band7, band8, band9, band10, band11]:
        # Open the files and store data in array.
		data[i] = s.tiff_to_array(lines, samples, the_folder, dFilenames[i])

	A_rho = {}
	M_rho = {}
	refl = {}
	refl_corr = {}
    #for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
	for i in [band1, band2, band3, band4, band5, band6, band7, band8, band9]:
		# Function to read in metadata and extract radiance, reflectance, K1, K2
		A_rho[i] = np.float(metadata['REFLECTANCE_ADD_BAND_%d' % i])
		M_rho[i] = np.float(metadata['REFLECTANCE_MULT_BAND_%d' % i])
		refl[i] = s.DN_to_refl(data[i], M_rho[i], A_rho[i])
		refl_corr[i] = s.reflectance_corrected(refl[i], np.float(metadata['SUN_ELEVATION']))

	rad = {}
	AL = {}
	ML = {}
	for i in [band1, band2, band3, band4, band5, band6, band7, band8, band9, band10, band11]:
		AL[i] = np.float(metadata['RADIANCE_ADD_BAND_%d' % i])
		ML[i] = np.float(metadata['RADIANCE_MULT_BAND_%d' % i])
		rad[i] = s.DN_to_radiance(data[i], ML[i], AL[i])
		#A_rho_6 = np.float(metadata['REFLECTANCE_ADD_BAND_%d' % band6])
		#M_rho_6 = np.float(metadata['REFLECTANCE_MULT_BAND_%d' % band6])
		
	
	K1 = {}
	K2 = {}
	BT = {}
	#for i in [10, 11]:
	for i in [band10, band11]:
		K1[i] = np.float(metadata['K1_CONSTANT_BAND_%d' % i])
		K2[i] = np.float(metadata['K2_CONSTANT_BAND_%d' % i])
		BT[i] = s.Radiance_to_satBT(data[i], rad[i], K1[i], K2[i])
	
	print(np.shape(BT[10]))
	print(np.shape(BT[11]))
	   
	#stack = np.concatenate([[lat_im], [lon_im], [refl[1]], [refl[2]], [refl[3]], [refl[4]], [refl[5]], [refl[6]], [refl[7]], [refl[8]], [refl[9]], [BT[10]], [BT[11]]])
	stack = np.concatenate([[lat_im], [lon_im], [refl_corr[1]], [refl_corr[2]], [refl_corr[3]], [refl_corr[4]], [refl_corr[5]], [refl_corr[6]], [refl_corr[7]], [data[9]], [BT[10]], [BT[11]]])

	print(np.shape(stack))

						#current     #Hartlepool #Dungeness #Hinckley #Hunterston-needs fix #Torness   #Sizewell  #Heysham
	center_lat = 54.028889 #54.635     #50.913889 #51.209   #55.726366-needs fix  #55.969752 #52.213461 #54.028889
	center_lon = -2.916111 #-1.180833  #0.963889  #-3.127   #-4.898619-needs fix  #-2.397156 #1.625419  #-2.916111
	dist_deg = 0.1
	dist_deg_smaller = 0.01
	spacing = 0.0005
	common_grid, min_lon, min_lat, spacing = p.creategrid(center_lat, center_lon , dist_deg, spacing)
	#common_grid_smaller, min_lon, min_lat, spacing = p.creategrid(center_lat, center_lon , dist_deg_smaller, spacing)
	print("common_grid shape", common_grid.shape)
	print(common_grid)
	

	#pdb.set_trace()
	data_regridded, count, distance = r.regridding(stack, min_lon, min_lat, spacing, common_grid.shape)
	#create a netcdf file
	print('data regridded shape' , data_regridded.shape)
	name = sys.argv[4] #'dungeness_LC08_L1TP_201025_20150418_20170409_01_T1'
	conv_nc.create_netcdf(name, data_regridded, common_grid[0,:,:], common_grid[1,:,:])
	"""
	#pdb.set_trace()  
	for i in range(11):
		plt.clf()
		plt.imshow(data_regridded[i,:,:], cmap='jet')
		plt.colorbar()
		#plt.clim(280,295)
		plt.title('05.06.2016 BAND%d' %(i+1))
		plt.savefig('heysham_05062016_band_%d.png' %(i+1))
	"""
#	pdb.set_trace()
	

if __name__ == "__main__":
    main(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
