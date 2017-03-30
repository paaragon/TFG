import trigonometry as tr

def hourAngle(doy, hora, lng, lstm):
	
	B = (doy - 81) * (360 / 365.0)
	eot = 9.87 * tr.sind(2 * B) - 7.53 * tr.cosd(B) - 1.5 * tr.sind(B)
	tc = 4 * (lng - lstm) + eot
	lst = hora + tc / 60.0

	hra = 15 * (lst - 12)

	return hra
