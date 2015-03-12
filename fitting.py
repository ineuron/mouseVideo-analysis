import numpy as np
from scipy import *
from scipy.optimize import leastsq


#model functions
def single_expl(x, params):
   # A * exp(-x/B) + C
   return(params[0] * exp(-x/float(params[1])) + params[2])

def sigmoid(x, params):
   # A/(1 + exp(-(x-B)*C))
   return(float(params[0])/(1 + exp(-(x-params[1])*params[2])))

#fitting functions
def errorfunc(params, x, data, fitfunc):
     fitfunc = functions[fitfunc]
     err = data - fitfunc(x, params)   
     return err

def fit_data(guess_params, x, data, fitfunc):
     fit_params = leastsq(errorfunc, guess_params, args=(x, data, fitfunc), full_output=1)
     return fit_params

functions = {
    'single_exponential': single_expl,
    'sigmoid': sigmoid
}

