import trigonometry as tr
import math

def robledoSoler(z):
	
	GHI = 1159.24 * pow(abs(tr.cosd(z)), 1.179) * math.exp(-0.0019 * (90 - abs(z)))

	return GHI
