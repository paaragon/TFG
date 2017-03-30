import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from zentihAngle import zentihAngle
from robledoSoler import robledoSoler
from kasten import kasten
from adnot import adnot
from dpp import dpp

def getGHI(fecha, hora, lat = 40.9904320, lng = -4.758942):
   
    doy = datetime.strptime(str(fecha), "%Y%m%d").timetuple().tm_yday
    print doy

    h = hora / 100 * 60
    h += hora % 100
    print h

    z, cosz = zentihAngle(lat, lng, doy - 1, h - 1)

    return robledoSoler(z)

if __name__ == "__main__":
    
    latNavas = 40.9904320
    logNavas = -4.7578942

    dias = range(365)
    horas = np.arange(0, 24, 1/60.0)
    
    GHIRS = dict()
    GHIKast = dict()
    GHIAdnot = dict()
    GHIDPP = dict()
    GHIMeinel = dict()
    
    #for doy in dias:
    doy = 0
    GHIRS[doy] = list()
    GHIKast[doy] = list()
    GHIAdnot[doy] = list()
    GHIDPP[doy] = list()
    
    for h in range(len(horas)):
        z, cosz = zentihAngle(latNavas, logNavas, doy, horas[h])
    
        GHIRS[doy].append(robledoSoler(z))   
        GHIKast[doy].append(kasten(cosz))
        GHIAdnot[doy].append(adnot(cosz))
        GHIDPP[doy].append(dpp(z, cosz))
    
    diasToPlot = [0]
    for i in range(0, len(diasToPlot)):
        d = diasToPlot[i]
    	titulo = "dia " + str(d)
    
    	robledo, = plt.plot(horas, GHIRS[d], label = 'Robledo-soler')
        kasten, = plt.plot(horas, GHIKast[d], label = 'Kast')
        adnot, = plt.plot(horas, GHIAdnot[d], label = 'Adnot')
        dpp, = plt.plot(horas, GHIDPP[d], label = 'DPP')
    
        plt.legend(handles=[robledo, kasten, adnot, dpp])
        plt.show()
