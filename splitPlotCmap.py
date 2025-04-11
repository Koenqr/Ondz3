import numpy as np
import matplotlib.pyplot as plt

import dataImporter

data0, data90 = dataImporter.getData()
#get vmin and vmax from data
vmin = min([min(x[2] for x in data0), min(x[2] for x in data90)])
vmax = max([max(x[2] for x in data0), max(x[2] for x in data90)])

#split figure into 2 subplots
fig, axs = plt.subplots(1, 2, figsize=(10,5), sharex=True, sharey=True)

#plt.rc('text', usetex=True)

ax0, ax90 = axs

x0 = np.array([x[0] for x in data0])
y0 = np.array([x[1] for x in data0]) - 90
z0 = np.array([x[2] for x in data0])
xi0, yi0 = np.meshgrid(np.unique(x0), np.unique(y0))
zi0 = ax0.tricontourf(x0, y0, z0, levels=100, cmap="turbo", vmin=vmin, vmax=vmax)
ax0.set_title("s-polarisatie")

x90 = np.array([x[0] for x in data90])
y90 = np.array([x[1] for x in data90]) - 90
z90 = np.array([x[2] for x in data90])
xi90, yi90 = np.meshgrid(np.unique(x90), np.unique(y90))
zi90 = ax90.tricontourf(x90, y90, z90, levels=100, cmap="turbo", vmin=vmin, vmax=vmax)
ax90.set_title("p-polarisatie")

#colorbar
cbar = fig.colorbar(zi0, ax=axs, orientation='vertical')
cbar.set_label("ADC lezing (V)")

#set axis labels (shared between subplots)
#ax0.set_xlabel(r"Incident angle $(\degree)$")
#ax0.set_ylabel(r"Detector angle $(\degree)$")
#ax90.set_xlabel(r"Incident angle $(\degree)$")

fig.supxlabel(r"Invals hoek $(\degree)$")
fig.supylabel(r"Detector hoek $(\degree)$")

plt.show()