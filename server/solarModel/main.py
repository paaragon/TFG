import matplotlib.pyplot as plt
import numpy as np
from zentihAngle import zentihAngle
from robledoSoler import robledoSoler

latNavas = 40.9904320
logNavas = -4.7578942

dias = range(365)
horas = np.arange(0, 24, 1/60.)
GHIRS = dict()

'''
GHIAdnot = dict()
GHIKast = dict()
GHIDPP = dict()
GHIMeinel = dict()
'''

for doy in dias:
	GHIRS[doy + 1] = list()
	for h in range(0, len(horas)):
		z, cosz = zentihAngle(latNavas, logNavas, doy, horas[h])
		GHIRS[doy + 1].append(robledoSoler(z))

		'''
		GHIKast[doy + 1, h] = kasten(cosz)
		GHIAdnot[doy + 1, h] = addnot(cosz)
		GHIDPP[doy + 1, h] = dpp(z, cosz)
		GHIMeinel[doy + 1, h] = meinel(cosz, extraTerretRad(doy))
		'''

print len(horas)
print len(GHIRS[1])

diasToPlot = [1, 8, 200]
for i in range(1, len(diasToPlot)):
	d = diasToPlot[i]
	titulo = "dia " + str(d)
	plt.plot(horas, GHIRS[d])
	plt.show()
