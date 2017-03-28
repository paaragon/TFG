import math
from declination import declination
from hourAngle import hourAngle

def zentihAngle(lat, lng, doy, hora):
	d = declination(doy)
	hra = hourAngle(doy, hora, lng, 0)
	cosz = math.cos(lat) * math.cos(d) * math.cos(hra) + math.sin(lat) * math.sin(d)
	z = math.acos(cosz)

	if(abs(z) > 90):
		z = 90
		cosz = 0

	return z, cosz