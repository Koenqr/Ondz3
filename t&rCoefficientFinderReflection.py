import numpy as np
import matplotlib.pyplot as plt
import lmfit

import dataImporter

#gaussian fit
def gaussian(x:float, amp, cen, wid, yo):
	"""Gaussian function."""
	return amp * np.exp(-(x - cen) ** 2 / (2 * wid ** 2)) + yo
def fitGaussian(x, y):
	"""Fit a Gaussian to the data."""
	# Create a model for the Gaussian function
	model = lmfit.Model(gaussian)
	
	# Set the initial parameter values
	params = model.make_params(amp=1, cen=np.mean(x), wid=1, yo=0)
	
	# Fit the model to the data
	result = model.fit(y, params, x=x)
	
	return result


splitDeg=90-15
#degs=[45,50,55,60,65,70,75]
degs=[50,55,60,65,70,75]

data0, data90 = dataImporter.getData()

points0 = []
points90 = []
upoints0 = []
upoints90 = []

for deg in degs:
	ldata0 = [ldata for ldata in data0 if ldata[0] == deg]
	ldata90 = [ldata for ldata in data90 if ldata[0] == deg]

	#split data for fitting at [1]>=splitDeg
	uldata0 = [ldata for ldata in ldata0 if ldata[1] >= splitDeg]
	uldata90 = [ldata for ldata in ldata90 if ldata[1] >= splitDeg]
	ldata0 = [ldata for ldata in ldata0 if ldata[1] < splitDeg]
	ldata90 = [ldata for ldata in ldata90 if ldata[1] < splitDeg]
 
	#find max power index
	maxPowerIndex0 = np.argmax([ldata[2] for ldata in ldata0])
	maxPowerIndex90 = np.argmax([ldata[2] for ldata in ldata90])
	umaxPowerIndex0 = np.argmax([ldata[2] for ldata in uldata0])
	umaxPowerIndex90 = np.argmax([ldata[2] for ldata in uldata90])
	
	#get data +-5 points around max power index
	spacing=5
	ldata0 = ldata0[maxPowerIndex0-spacing:maxPowerIndex0+spacing+1]
	ldata90 = ldata90[maxPowerIndex90-spacing:maxPowerIndex90+spacing+1]
	uldata0 = uldata0[umaxPowerIndex0-spacing:umaxPowerIndex0+spacing+1]
	uldata90 = uldata90[umaxPowerIndex90-spacing:umaxPowerIndex90+spacing+1]
	fig=plt.figure(figsize=(10, 5))
	ax=fig.add_subplot(111)
	ax.scatter([ldata[1] for ldata in uldata0], [ldata[2] for ldata in uldata0], label='0° reflectie', color='cyan')
	plt.show()
	
 
	#sort by x
	ldata0.sort(key=lambda x: x[1])
	ldata90.sort(key=lambda x: x[1])
	uldata0.sort(key=lambda x: x[1])
	uldata90.sort(key=lambda x: x[1])
	lx0 = np.array([ldata[1] for ldata in ldata0])
	ly0 = np.array([ldata[2] for ldata in ldata0])
	ux0 = np.array([ldata[1] for ldata in uldata0])
	uy0 = np.array([ldata[2] for ldata in uldata0])
	lx90 = np.array([ldata[1] for ldata in ldata90])
	ly90 = np.array([ldata[2] for ldata in ldata90])
	ux90 = np.array([ldata[1] for ldata in uldata90])
	uy90 = np.array([ldata[2] for ldata in uldata90])
	
	#fit data
	result0 = fitGaussian(lx0, ly0)
	result90 = fitGaussian(lx90, ly90)
	resultu0 = fitGaussian(ux0, uy0)
	resultu90 = fitGaussian(ux90, uy90)
	
	fig=plt.figure(figsize=(10, 5))
	ax=fig.add_subplot(111)
	ax.scatter(lx0, ly0, label='0°', color='blue')
	#add gaussian fit to plot
	ax.plot(lx0, result0.eval(x=lx0), 'r-', label='fit 0°')
	plt.show()
 
	points0.append((deg, result0))
	points90.append((deg, result90))
	upoints0.append((deg, resultu0))
	upoints90.append((deg, resultu90))
 


degError=2 
#plot data (power over angle)
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)

#process points for plotting x:degs, y: fit amp + yo
#ax.plot([point[0] for point in points0], [point[1].params['amp'].value + point[1].params['yo'].value for point in points0], label='0°', color='blue')
#ax.plot([point[0] for point in points90], [point[1].params['amp'].value + point[1].params['yo'].value for point in points90], label='90°', color='red')
#ax.plot([point[0] for point in upoints0], [point[1].params['amp'].value + point[1].params['yo'].value for point in upoints0], label='0° (reflectie)', color='cyan')
#ax.plot([point[0] for point in upoints90], [point[1].params['amp'].value + point[1].params['yo'].value for point in upoints90], label='90° (reflectie)', color='magenta')

ax.errorbar([point[0] for point in points0], [point[1].params['amp'].value + point[1].params['yo'].value for point in points0], xerr=degError)#, yerr=[point[1].params['amp'].stderr + point[1].params['yo'].stderr for point in points0], label='0°', color='blue', fmt='o')


plt.legend()
plt.show()