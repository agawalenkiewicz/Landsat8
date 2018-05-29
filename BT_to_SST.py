import math as m
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.image as mpimg
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
from sklearn import linear_model
import sys

def arrayToSST(dBTs10, dBTs11):
	"""
	Combine the raw digital numbers (DN) of band 10 and 11 into an SST array.
	"""
    # Combine the BTs into an SST
	aSST = btToSST(dBTs10, dBTs11)
	return aSST


def btToSST(aB10, aB11):
    # Get the coefficients for a linear combination.
	fIntcpt, fB10Coeff, fB11Coeff = findSSTCoeffcients()
	aSST = fIntcpt + fB10Coeff * aB10 + fB11Coeff * aB11
    # Convert Kelvin to Celcius
	#aSST -= 273.15
	return aSST
	
def findSSTCoeffcients():
	"""
	Use radiative transfer model (RTM) data to calculate the optimum
	combination of B10 and B11 brightness temperatures to retrieve SST.
	"""

    # Open RTM CSV file.
	CSVFile = sys.argv[2] #("N:/getting_netcdf/bts_rtcoef_landsat_8_tirs.csv")
	CSV = mlab.csv2rec(CSVFile)
	vSST = CSV.sst
	vLat = CSV.lat
	vB10 = CSV.b10
	vB11 = CSV.b11

    # Remove points which fall outside of mid-latitudes.
	points_delete = []
	for i in xrange(len(vLat)):
		if abs(vLat[i]) < 35.0 or abs(vLat[i]) > 65.0:
			points_delete.append(i)

	vSST = np.delete(vSST, points_delete)
	vLat = np.delete(vLat, points_delete)
	vB10 = np.delete(vB10, points_delete)
	vB11 = np.delete(vB11, points_delete)

    # Calculate least-squares fit between B10 and B11 data and the SSTs.
    # See http://stackoverflow.com/questions/19991445/
    # run-an-ols-regression-with-pandas-data-frame
	G = np.vstack((vB10, vB11))
	oCLF = linear_model.LinearRegression()
	oCLF.fit(G.T, vSST)

	Intcpt = oCLF.intercept_
	B10Coeff = oCLF.coef_[0]
	B11Coeff = oCLF.coef_[1]

	vReconstructed = Intcpt + B10Coeff * vB10 + B11Coeff * vB11
	vError = vSST - vReconstructed
	RMSE = np.sqrt(np.mean(vError**2))

	print "-- No. points used:", len(vSST)
	print "-- RMSE: {:.2f}".format(RMSE)
	print "-- R^2 fit: {:.2f}".format(oCLF.score(G.T, vSST))
	print ("-- Intercept: {:.2f}; B10 coeff.: {:.2f}; " "B11 coeff.: {:.2f}".format(Intcpt, B10Coeff, B11Coeff))

	return Intcpt, B10Coeff, B11Coeff

# read in the netcdf file, file given as argument in the command line	
filename = sys.argv[1]	
#dataset = nc.Dataset(filename)
dataset = nc.Dataset(filename, 'r+' , format="NETCDF4")

BT_band10_masked = np.array(dataset.variables['BT10_masked'])
BT_band11_masked = np.array(dataset.variables['BT11_masked'])

# Convert DN to BT to SST.
aSST = arrayToSST(BT_band10_masked, BT_band11_masked)

lat = dataset.dimensions['lat'] 
lon = dataset.dimensions['lon']
# Create the actual 4-d variable
#SST = dataset.createVariable('SST', np.float32, ('lat','lon'))
SST = dataset.variables['SST']
#bands.units = 'micro_meters'
SST.units = 'K' #'deg C'
#Assign values to the variables
SST[:,:] = aSST
#Close dataset
dataset.close()