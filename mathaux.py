'''
Mathaux:
Auxilary mathematical functions used in data analysis. 
'''
import numpy as np
import math
def evalPoly(poly, x):
    res = 0.0
    for k in range(0, len(poly)):
        res += poly[-(k+1)] * x ** k
    return res

def printPoly(poly):
    res = []
    for k in range(0, len(poly)):
        res.append(str(poly[-(k+1)]) + "x" + "^" + str(k))
    res.reverse()
    print(*res)

def errorPoly(obs_dat, poly, param, norm_scl=0, norm_off=-0):
    '''
    :param: obs_dat : a numpy array that has the original observed values of the data.
    :param: poly : the polynomial relation whose value is to be compared with the observed data.
    :param: param : a numpy array with values of 'x' in it for which the observations are availible.
    :param: norm_scl : this is the normalization scale that will be applied on the 'y' values
    :param: norm_off : this is the normalisation offset that will be applied on the 'y' values for shifting the origin.
    '''
    vals = np.array([evalPoly(poly, param[k]) for k in range(0,len(param))])
    vals = (vals / 10 ** norm_scl) + norm_off # Shift the scale and origin to the original reference.
    sum_del = sum([(vals[k] - obs_dat[k]) ** 2 for k in range(0,len(obs_dat))])
    div = math.sqrt(sum_del/len(obs_dat)) # The root mean squared error.
    return div

def solvePoly(poly, y):
    coeff = poly.copy()
    coeff[-1] -= y
    return np.roots(coeff)
