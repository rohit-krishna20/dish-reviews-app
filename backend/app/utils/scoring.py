from math import sqrt

def bayes_score(mean: float, n: int, global_mean: float=4.0, m: int=20) -> float:
    if n<=0: return 0.0
    return (n/(n+m))*mean + (m/(n+m))*global_mean

def wilson_lower_bound(pos: int, n: int, z: float=1.96) -> float:
    if n==0: return 0.0
    phat = pos/n
    denom = 1 + z*z/n
    centre = phat + z*z/(2*n)
    margin = z*sqrt((phat*(1-phat)+z*z/(4*n))/n)
    return (centre - margin)/denom
