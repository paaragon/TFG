import trigonometry as tr

def declination(doy):
	
	B = (doy - 81) * (360 / 365.0)
	d = 23.45 * tr.sind(B)

	return d
