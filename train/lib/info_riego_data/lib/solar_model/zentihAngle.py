import trigonometry as tr
import math
from declination import declination
from hourAngle import hourAngle

def zentihAngle(lat, lng, doy, hora):

	d = declination(doy) #in radians

        hra = hourAngle(doy, hora, lng, 0) #in radians

	cosz = tr.cosd(lat) * tr.cosd(d) * tr.cosd(hra) + tr.sind(lat) * tr.sind(d)

	z = tr.acosd(cosz)

	if(abs(z) > 90):
		z = 90
		cosz = 0

	return z, cosz
