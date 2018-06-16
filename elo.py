import math
from config import ELO_K as K

def elo_probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def elo_rating(ra, rb, K):

    pb = elo_probability(ra, rb)

    pa = elo_probability(rb, ra)

    ra = round(ra + K * (1 - pa),0)
    rb = round(rb + K * (0 - pb),0)

    return (ra,rb)
