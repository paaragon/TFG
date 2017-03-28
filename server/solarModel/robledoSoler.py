import math

def robledoSoler(z):
	
	GHI = 1159.24 * abs(math.cos(z)) ** 1.179 * math.exp(-0.0019 * (90 - abs(z)))

	return GHI