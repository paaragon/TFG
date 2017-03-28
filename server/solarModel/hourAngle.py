import math

def hourAngle(doy, hora, lng, lstm):
	
	B = (doy - 81) * (360 / 365.)
	eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
	tc = 4 * (lng - lstm) + eot
	lst = hora + tc / 60.
	hra = 15 * (lst - 2)

	return hra