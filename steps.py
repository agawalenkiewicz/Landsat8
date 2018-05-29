# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:11:48 2017

@author: Agnieszka
"""
import matplotlib.pyplot as plt
import numpy as np
import math

import netCDF4 as nc
from netCDF4 import Dataset

import glob

#from osgeo import gdal
#from osgeo import osr
import gdal
import osr

import os

import copy
import sys


def latlon_image(Filepath, Filename):

	# Open input dataset
	filenames = os.path.join(Filepath, Filename)
	indataset = gdal.Open( filenames, gdal.GA_ReadOnly )
  
	# Read geotransform matrix and calculate ground coordinates
	geomatrix = indataset.GetGeoTransform()
	pixel = indataset.RasterXSize
	line = indataset.RasterYSize
	#WGS coordinate system
	wgs84_wkt = """
    GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""

	new_coord_sys = osr.SpatialReference()
	new_coord_sys.ImportFromWkt(wgs84_wkt)
 
	# Build Spatial Reference object based on coordinate system, fetched from the
	# opened dataset
	srs = osr.SpatialReference()
	srs.ImportFromWkt(indataset.GetProjection())
  
	srsLatLong = srs.CloneGeogCS()
	ct = osr.CoordinateTransformation(srs, new_coord_sys)
	
	lat_im = np.zeros([line, pixel])
	lon_im = np.zeros([line, pixel])
	
	for i in np.arange(0, line,1):
		for j in np.arange(0, pixel,1):
			X = geomatrix[0] + geomatrix[1] * j + geomatrix[2] * i
			Y = geomatrix[3] + geomatrix[4] * j + geomatrix[5] * i
  
			# Shift to the center of the pixel
			X += geomatrix[1] / 2.0
			Y += geomatrix[5] / 2.0
  	
			#(int, lat, height) = ct.TransformPoint(X, Y)
			(latlon) = ct.TransformPoint(X, Y)
			#lat_im[i,j] = lat
			#lon_im[i,j] = int
			lat_im[i,j] = (latlon[1])
			lon_im[i,j] = (latlon[0])
			#print('%g, %g' % (i,j))
			# Report results
			#print('pixel: %g\t\t\tline: %g' % (pixel, line))
			#print('latitude: %fd\t\tlongitude: %fd' % (lat, int))
			#print('latitude: %s\t\tlongitude: %s' % (gdal.DecToDMS(lat, 'Lat', 2), gdal.DecToDMS(int, 'Long', 2)))
	#lat_im = np.flipud(lat_im) # flip latitudes upside down so that it starts at 53 and ends at 55 degrees...
	return(lat_im, lon_im)


def read_info(Filepath, Filename):
	"""
	This function reads in the file and gets information 
	about the coordinate system, and x and y origin of the point
	"""
	filenames = os.path.join(Filepath, Filename)
	dataset = gdal.Open(filenames, gdal.GA_ReadOnly)
	geotransform = dataset.GetGeoTransform()
	#get the origin points of the image
	width = dataset.RasterXSize
	height = dataset.RasterYSize
	x = geotransform[0] #+ width*geotransform[1] + height*geotransform[2]
	y = geotransform[3] #+ width*geotransform[4] + height*geotransform[5]
	#get the existing coordinate system
	old_coord_sys = osr.SpatialReference()
	old_coord_sys.ImportFromWkt(dataset.GetProjectionRef())
	dataset.ReadAsArray()
	return x, y, old_coord_sys, dataset

#print read_info(the_file)[2]



def transform(old_coord_sys):
    """
    This function converts the old (original) coordinate
    system into a new one. Apart from that, it returns an object
    called transform that can be used later to change coordinates
    of the points in the file. (maybe transform should be in the next function?)
    """
    wgs84_wkt = """
    GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""

    new_coord_sys = osr.SpatialReference()
    new_coord_sys.ImportFromWkt(wgs84_wkt)

    #create a transform object to convert bewteen the coordinate systems
    transform = osr.CoordinateTransformation(old_coord_sys, new_coord_sys)
    return(transform)




#def change_coord(x_origin, y_origin, transform):
def change_coord(lines, samples, x, y, transform):
    """
    This function takes as input the x and y origins of the point
    from the original coordinate system.
    It returns a 2D array of new coordinates for all points.
    """
    new_coord = []
    lat = np.zeros([lines, samples])
    lon = np.zeros([lines, samples])
    #lat = np.zeros([8061, 7981])
    #lon = np.zeros([8061, 7981])
    #for i in np.arange(0,8061,1):
    for i in np.arange(0, lines, 1):
        #for j in np.arange(0,7981,1):
        for j in np.arange(0, samples, 1):
            latlon = transform.TransformPoint(i+x,j+y)
            #new_coord.append(latlon)
            # returns as list, should return as 2D array
            lat[i,j] = (latlon[0])
            lon[i,j] = (latlon[1])
    return(lat, lon)
    


def get_metadata(Filepath, Filename):
    myfile = os.path.join(Filepath, Filename)
    meta = {}
    with open(myfile) as file:
        for line in file:
            name, var = line.partition("=")[::2]
            meta[name.strip()] = var
    return meta

	
def tiff_to_array(lines, samples, Filepath, Filename):
    """
    Open the TIFF file and store in an array.
    """
    object_image = plt.imread("{}/{}".format(Filepath, Filename))
    array_image = np.array(object_image[0:lines,0:samples])
    array_image = array_image.astype(np.float)
    array_image = np.ma.array(array_image, mask=array_image == 0.0)
    return array_image

	
def DN_to_refl(image_data, M_ro, A_ro):
    #https://landsat.usgs.gov/landsat-8-l8-data-users-handbook-section-5
    """
    Convert the DN to TOA Reflectance as described in primer document.
    NOTE THESE ARE UNCORRECTED FOR SUN ANGLE.
    M_rho = Band-specific multiplicative rescaling factor from the metadata
        (REFLECTANCE_MULT_BAND_x, where x is the band number)
    A_rho = Band-specific additive rescaling factor from the metadata
        (REFLECTANCE_ADD_BAND_x, where x is the band number)
    """

    M_ro = 2.0E-05
    A_ro = -0.1

    Reflectance = np.ma.copy(image_data)
    Reflectance *= M_ro
    Reflectance += A_ro

    return Reflectance

def reflectance_corrected(refl, sun_elev_angle):
	"""
    Correct TOA Reflectance (array) for Sun angle as described in primer document.
    sun_elev_angle  = sun elevantion angle (from metadata file) - single number
	sun_zenith_angle = solar zenith angle (90 deg - sun_elev_angle) - single number
    """
	sun_zenith_angle = 90 - sun_elev_angle
	Reflectance_corr = refl / (math.cos(sun_zenith_angle))
	
	return Reflectance_corr

	
def DN_to_radiance(image_data, ML, AL):
    """
    Take raw data and convert to TOA Radiance using method described in
    Landsat8 Primer document.
    """

    # Band-specific multiplicative rescaling factor from the metadata
    # (RADIANCE_MULT_BAND_x, where x is the band number)
    #ML = 3.3420E-04

    # Band-specific additive rescaling factor from the metadata
    # (RADIANCE_ADD_BAND_x, where x is the band number)
    #AL = 0.1

    Radiance = image_data * ML
    Radiance += AL

    return Radiance


def Radiance_to_satBT(image_data, Radiance, K1, K2):
    #https://landsat.usgs.gov/landsat-8-l8-data-users-handbook-section-5
    """
    Convert TOA Radiance to At-Satellite Brightness Temperature (BT).

    K1 = Band-specific thermal conversion constant from the metadata
    (K1_CONSTANT_BAND_x, where x is the band number, 10 or 11)

    Band-specific thermal conversion constant from the metadata
    (K2_CONSTANT_BAND_x, where x is the band number, 10 or 11)
    """
    #K1 = 774.89
    #K2 = 1321.08

    satBT = np.ma.masked_where(image_data == 0.0, image_data)

    satBT = K1 / Radiance
    satBT += 1.0
    satBT = np.log(satBT)
    satBT = K2 / satBT

    return satBT
#print change_coord(read_info(the_file)[0], read_info(the_file)[1], transform(read_info(the_file)[2]))
