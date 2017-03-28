import math

def declination(doy):
	
	B = (doy - 81) * (360 / 365.)
	d = 23.45 * math.sin(B)

	return d