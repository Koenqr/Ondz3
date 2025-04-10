import numpy as np
import matplotlib.pyplot as plt
import lmfit
import typing


import dataImporter


data0, data90 = dataImporter.getData()

#setup lmfit model for gaussian
def gaussian(x:float, amp, cen, wid, yo):
	"""Gaussian function."""
	return amp * np.exp(-(x - cen) ** 2 / (2 * wid ** 2)) + yo
def fitGaussian(x, y):
	"""Fit a Gaussian to the data."""
	# Create a model for the Gaussian function
	model = lmfit.Model(gaussian)
	
	# Set the initial parameter values
	params = model.make_params(amp=1, cen=np.mean(x), wid=1, yo=min(y))
	
	# Fit the model to the data
	result = model.fit(y, params, x=x)
	
	return result


#setup snellius law fit #np.rad2deg(np.arcsin(np.sin(np.radians(x))/1.54))-x
def snellius(x, n):
	"""Snellius law function."""
	return np.rad2deg(np.arcsin(np.sin(np.radians(x))/n))-x
def fitSnellius(x, y, weight=None):
	"""Fit Snellius law to the data."""
	# Create a model for the Snellius function
	model = lmfit.Model(snellius)
	
	# Set the initial parameter values
	params = model.make_params(n=1.54)
	
	# Fit the model to the data
	result = model.fit(y, params, x=x, weights=weight)
	
	return result



#create dict of data {degs: (deg,mean,stdev)}
degs=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75)

max0 = {}
max90 = {}

for data in data0:
	if max0.get(data[0]) is None:
		max0[data[0]] = data
	elif max0[data[0]][2] < data[2]:
		max0[data[0]] = data

for data in data90:
	if max90.get(data[0]) is None:
		max90[data[0]] = data
	elif max90[data[0]][2] < data[2]:
		max90[data[0]] = data



#get +-20 degrees from max and fit gaussian using curve_fit

points0 = []
points90 = []
for deg in degs:
	#s-polarization
	ldata0 = [ldata for ldata in data0 if ldata[0] == deg]
	ldata90 = [ldata for ldata in data90 if ldata[0] == deg]
 
	#get data +-20 degrees
	ldata0 = [ldata for ldata in ldata0 if ldata[1] >= max0[deg][1]-20 and ldata[1] <= max0[deg][1]+20]
	ldata90 = [ldata for ldata in ldata90 if ldata[1] >= max90[deg][1]-20 and ldata[1] <= max90[deg][1]+20]
 
	#sortdata by x
	ldata0 = sorted(ldata0, key=lambda x: x[1])
	ldata90 = sorted(ldata90, key=lambda x: x[1])
	
	#fit gaussian
	x0 = np.array([ldata[1] for ldata in ldata0])
	y0 = np.array([ldata[2] for ldata in ldata0])
	x90 = np.array([ldata[1] for ldata in ldata90])
	y90 = np.array([ldata[2] for ldata in ldata90])
	#fit gaussian
	result0 = fitGaussian(x0, y0)
	result90 = fitGaussian(x90, y90)
	#append to points (degs, cen, stdev)
	points0.append((deg, result0.params["cen"].value, result0.params["wid"].value))
	points90.append((deg, result90.params["cen"].value, result90.params["wid"].value))
	
	



#1,2 scatter plot

fig, axs = plt.subplots(1, 2, figsize=(10,5), sharex=True, sharey=True)
ax0, ax90 = axs

xerr = 2

#scatter of x=degs y=cen from fit with error bars xerr=2 yerr=stdev
x0 = np.array([point[0] for point in points0])
y0 = np.array([point[1] for point in points0])-90
yerr0 = np.array([point[2] for point in points0])
x90 = np.array([point[0] for point in points90])
y90 = np.array([point[1] for point in points90])-90
yerr90 = np.array([point[2] for point in points90])
y0=y0-y0[0] #centering due to incident angle and exit angle being 0 at 0 degrees
y90=y90-y90[0]
ax0.errorbar(x0, y0, xerr=xerr, yerr=yerr0, fmt=".", label="s-polarisatie")
ax90.errorbar(x90, y90, xerr=xerr, yerr=yerr90, fmt=".", label="p-polarisatie")
ax0.set_title("s-polarisatie")
ax90.set_title("p-polarisatie")


#fit snellius law
result0 = fitSnellius(x0, y0, weight=1/yerr0)
result90 = fitSnellius(x90, y90, weight=1/yerr90)
print("-------------------------------------------")
print("Snellius law fit results:")
print("s-polarization:")
print(result0.fit_report())
print("p-polarization:")
print(result90.fit_report())
print("-------------------------------------------")

#fit snellius to both data sets at once
result = fitSnellius(np.concatenate((x0, x90)), np.concatenate((y0, y90)), weight=np.concatenate((1/yerr0, 1/yerr90)))

print("Snellius law fit results (both):")
print(result.fit_report())
print("-------------------------------------------")



#plot fit
x = np.linspace(0, 75, 100)
y = result0.eval(x=x)
ax0.plot(x, y, color=(255/255, 0/255, 255/255), label=f"Snellius fit (n={result0.params['n'].value:.3f} $\pm$ {result0.params['n'].stderr:.3f})")
y = result90.eval(x=x)
ax90.plot(x, y, color=(255/255, 0/255, 255/255), label=f"Snellius fit (n={result90.params['n'].value:.3f} $\pm$ {result90.params['n'].stderr:.3f})")

ax0.legend()
ax90.legend()

fig.supxlabel(r"Hoek van inval $(\degree)$")
fig.supylabel(r"Hoek van uitval $(\degree)$")

plt.tight_layout()
plt.show()