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

import matplotlib.dates as mdates

def read_datafile(file_name):
	"""
	This function reads in a csv file. It returns them as a numpy array.
	"""
	data = np.genfromtxt(file_name, delimiter=',')
	return data

def read_dates(text_file):
	"""
	This function reads in a text file with dates obtained from a bash script.
	The bash script returns a csv file, where all odd rows (i.e. 1,3,5,...)
	have a date in the format YYYYMMDD and every even row (i.e. 2,4,6,...)
	has a converted, human readable date.
	This function takes the whole csv file. It searched only for human readable dates
	and treats each element of the date as a string. It then combines all strings 
	and puts a reasonable space between the words.
	It returns a list of human readable dates, where each date is a speerate list element.
	"""
	#dates = np.genfromtxt(text_file , usecols=[1,2,3], invalid_raise=False, dtype="S10")
	dates = np.genfromtxt(text_file , usecols=[0], invalid_raise=False, dtype="S10")
	dates = dates[0::2]
	datum = []
	for i in dates:
		#date = (i[0]).ljust(4) + (i[1]).ljust(3) + (i[2]).ljust(5) #+ (i[3])
		#datum.append(date)
		datum.append(i)
	return datum

def plot_inflow_outflow(inflow10, inflow11, outflow10, outflow11, diff10, diff11, time, place):
	"""
	This function plots the different BT of the inflow point, outflow point and difference.
	There are 3 subplots. First is for inflow BT, second for outflow BT and third for difference.
	"""
	fig = plt.figure()
	
	days_format = mdates.DateFormatter('%d/%m/%Y')
	days_loc = mdates.DayLocator()
	my_xticks = time
	ax1 = fig.add_subplot(211)
	

	ax1.set_title("BT of Inflow and the Outflow points")    
	ax1.set_xlabel('scenes (last to newest)')
	ax1.set_ylabel('BT [K]')

	ax1.plot(time, inflow10, '--', c='r', label='inflow T 10.8 micron')
	ax1.plot(time, inflow11, '--', c='b', label='inflow T 12 micron')
	ax1.plot(time, outflow10, '-', c='r', label='outflow T 10.8 micron')
	ax1.plot(time, outflow11, '-', c='b', label='outflow T 12 micron')
	ax1.xaxis.set_major_locator(days_loc)
	ax1.xaxis.set_major_formatter(days_format)
	ax1.get_xaxis()
	#ax1.get_xaxis().set_visible(False)
	ax1.set_xticks(time)
	_=plt.xticks(rotation=90, fontsize='small')
	#leg = ax1.legend()
	ax1.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0. , fontsize='small')

	

	ax2 =fig.add_subplot(212)

	ax2.set_title("BT difference between Outflow and Inflow point")    
	ax2.set_xlabel('scenes (last to newest)')
	ax2.set_ylabel('BT [K]')

	ax2.plot(time, diff10, c='r', label='10.8 micron')
	ax2.plot(time, diff11, c='b', label='12 micron')
	#ax2.xaxis.set_major_locator(days)
	ax2.xaxis.set_major_formatter(days_format)
	ax2.get_xaxis()
	ax2.set_xticks(time)
	_=plt.xticks(rotation=90, fontsize='small')
	#leg3 = ax3.legend()
	ax2.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0. , fontsize='small')

	fig.subplots_adjust(hspace=0.5)
	plt.suptitle(place, fontsize=16)
	plt.show()
	plt.savefig('timeseries.png')

def plotBTs(x,y):

	fig1 = plt.figure()
###    
	plt.plot(x, y-x, 'o', markersize=2)
	plt.xlim([265,300])
	plt.ylim([-5,0])
	plt.xlabel('Brightness Temperature 10.8 Micron Channel')
	plt.ylabel('Brightness Temperature 12 - 10.8 Micron')
	fig1.suptitle('BT Differences')
	plt.savefig('scatter_difference_jake.png')
###
	fig2 = plt.figure()
	m,c = np.polyfit(x,y,1)
	print m,c
	ynew = (m*x)+c
	plt.plot(x,ynew,'-')
	plt.plot(278,278,'x',markersize=100)
	fig2.suptitle('Best Fit')
	plt.xlabel('Brightness Temperature 10.8 Micron Channel')
	plt.ylabel('Brightness Temperature 12 - 10.8 Micron Channel')
	plt.savefig('Best_fit_jake.png')
  
def histBTs(x,y):
    
	plt.figure()
	plt.hist2d(x, (y-x),(55,55),([265,300],[-5,0]), cmap=plt.cm.gist_ncar)
	plt.xlabel('10.8 Micron Channel BT')
	plt.ylabel('12 Micron Channel BT')
	cbar = plt.colorbar()
	cbar.ax.set_ylabel('Counts')     
	plt.savefig('Hist_diff_jake.png')
	
def show_images(place, date, images, titles = None, cols = 1):
	"""Display a list of images in a single figure with matplotlib.
    
	Parameters
	---------
	images: List of np.arrays compatible with plt.imshow.
    
	cols (Default = 1): Number of columns in figure (number of rows is 
	set to np.ceil(n_images/float(cols))).
    
	titles: List of titles corresponding to each image. Must have
	the same length as titles.
	"""
	assert((titles is None)or (len(images) == len(titles)))
	n_images = len(images)
	if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
	fig = plt.figure()
	for n, (image, title) in enumerate(zip(images, titles)):
		a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        #if image.ndim == 2:
            #plt.gray()
		plt.imshow(image, cmap='jet')
		a.set_title(title)
		# create an axes on the right side of ax. The width of cax will be 5%
		# of ax and the padding between cax and ax will be fixed at 0.05 inch.
		ax = plt.gca()
		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cbar = plt.colorbar(cax=cax)
		# add label to the colourbar and limits
		cbar.set_label('Temp [K]', size=10)
		plt.clim(270,295)
	fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
	plt.subplots_adjust(top=0.99)
	#plt.tight_layout()
	#adjust the width and height between the subplots
	plt.subplots_adjust(wspace=0.3, hspace=0.3)
	plt.suptitle(place+' '+date, fontsize=20)
	plt.show()
	
#all files to be used in this python program
# are entered in the comman line as follows:
# BT of inflow at 10.8 and 12 microns - sys.argv[1] and sys.argv[2]
# BT of outflow at 10.8 and 12 microns - sys.argv[3] and sys.argv[4]
# dates of all scenes for a specifis site - sys.argv[5]

in_data_band10 = read_datafile(sys.argv[1])
in_data_band11 = read_datafile(sys.argv[2])
out_data_band10 = read_datafile(sys.argv[3])
out_data_band11 = read_datafile(sys.argv[4])
dates = read_dates(sys.argv[5])
location_name = sys.argv[6]

# create a list of dates and correspoding temperature 
#(measured on that day) of inflow and outflow
l = [dates, in_data_band10, in_data_band11, out_data_band10, out_data_band11]
measurements = map(list, zip(*l))

measurements_sorted = (sorted(measurements, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'), reverse=False))
print measurements_sorted


time = []
in_b10 = []
in_b11 = []
out_b10 = []
out_b11 = []
for i in range(len(measurements_sorted)):
	#print measurements_sorted[i][0]
	#print measurements_sorted[i][1]
	time.append(measurements_sorted[i][0])
	in_b10.append(measurements_sorted[i][1])
	in_b11.append(measurements_sorted[i][2])
	out_b10.append(measurements_sorted[i][3])
	out_b11.append(measurements_sorted[i][4])

print time
#print in_b10
#print out_b11
time = [datetime.strptime(i, '%d/%m/%Y') for i in time]
print time
#difference between BT at outflow and inflow can be calculated
# however, it is not the best idea
# as inflow is not at surface but at depth
diff_b10 = np.array(out_b10) - np.array(in_b10)
diff_b11 = np.array(out_b11) - np.array(in_b11)	

plot_inflow_outflow(in_b10, in_b11, out_b10, out_b11, diff_b10, diff_b11, time, location_name)

"""

# read in the netcdf file, file given as argument in the command line	
filename = sys.argv[1]	
nc_file = nc.Dataset(filename)
dataset = nc.Dataset(filename)

lons = np.array(dataset.variables['longitude'])
lats = np.array(dataset.variables['latitude'])
BT_band10 = np.array(dataset.variables['BT_band10'])
BT_band11 = np.array(dataset.variables['BT_band11'])
BT_band10_masked = np.array(dataset.variables['BT10_masked'])
BT_band11_masked = np.array(dataset.variables['BT11_masked'])
SST = np.array(dataset.variables['SST'])
SSTMask = ma.masked_where(SST > 300, SST)


place = sys.argv[2]
date = sys.argv[3]
image_list = [BT_band10_masked, BT_band11_masked, SSTMask]
title_list = ['BT 10.8 micron', 'BT 12 micron', 'SST']
show_images(place, date, image_list, title_list)


#aBT10 = np.ma.masked_where(BT_band10_masked == 0, BT_band10_masked)
#aBT11 = np.ma.masked_where(BT_band11_masked == 0, BT_band11_masked)

#plotBTs(BT_band10_masked.flatten(), BT_band11_masked.flatten())
#histBTs(BT_band10_masked.flatten(), BT_band11_masked.flatten())


# Plots BT 10 and 11 against one another#
dBT10 = BT_band10.flatten()
dBT10 = np.ravel(dBT10)
dBT11 = BT_band11.flatten()
dBT11 = np.ravel(dBT11)
gd_data = (dBT10<1020)*(dBT11<1020)
plotBTs(dBT10[gd_data], dBT11[gd_data])
### Plot Histograms ###

# Plots histogram of 10 and 11 BTs#
x = BT_band10.flatten()
hBTx = np.ravel(x)
y = BT_band11.flatten()
hBTy = np.ravel(y)
good_data = (hBTx < 1020)*(hBTy < 1020)
histBTs(hBTx[good_data], hBTy[good_data])
"""
