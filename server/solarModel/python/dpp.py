import math

def dpp(z, cosz):

    dni = 950.2 * (1 - math.exp(-0.075 * (90 - abs(z))))
    diff = 14.29 + 21.04 * (math.pi / 2.0 - abs(z) * math.pi / 180.0)
    ghi = dni * abs(cosz) + diff

    return ghi
