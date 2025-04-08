import typing


'''
base=("START SERIES "," deg.txt")
degs=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75)

#define data structure such that csv (; separated) is imported as (degs,deg,mean,stdev)
data = []
for deg in degs:
	with open("90/"+base[0]+str(deg)+base[1]) as f:
		for line in f:
			data.append((deg,)+tuple(map(float,line.split(";"))))
'''



def getData():
	base=("START SERIES "," deg.txt")
	degs=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75)
	data0 = []
	data90 = []
	for deg in degs:
		with open("90/"+base[0]+str(deg)+base[1]) as f:
			for line in f:
				data0.append((deg,)+tuple(map(float,line.split(";"))))
		with open("0/"+base[0]+str(deg)+base[1]) as f:
			for line in f:
				data90.append((deg,)+tuple(map(float,line.split(";"))))
	return data0, data90