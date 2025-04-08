import matplotlib.pyplot as plt
import numpy as np


base=("START SERIES "," deg.txt")
degs=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75)

#define data structure such that csv (; separated) is imported as (degs,deg,mean,stdev)
data = []
for deg in degs:
	with open("90/"+base[0]+str(deg)+base[1]) as f:
		for line in f:
			data.append((deg,)+tuple(map(float,line.split(";"))))



choice="1"#input("Choose type of plot")

if choice=="1":


	#plot as heat map (x:deg, y:degs, z:mean)
	fig=plt.figure()
	ax=fig.add_subplot(111)


	x = np.array([x[0] for x in data])
	y = np.array([x[1] for x in data])-90
	z = np.array([x[2] for x in data])

	xi, yi = np.meshgrid(np.unique(x), np.unique(y))
	zi = ax.tricontourf(x, y, z, levels=20, cmap="turbo")
	plt.colorbar(zi, ax=ax, label="ADC reading (V)")
	#generate line (snells law) n=1.54 to overlay
	x = np.linspace(0,75,100)
	y = np.rad2deg(np.arcsin(np.sin(np.radians(x))/1.54))-x
	ax.plot(x,y, color=(255/255, 0/255, 255/255), label="Snell's Law n=1,54")

	ax.set_xlabel("Angle of incidence (deg)")
	ax.set_ylabel("Detector angle (deg)")

	plt.show()