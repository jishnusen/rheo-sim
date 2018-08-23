from tkinter import filedialog
import tkinter

tkinter.Tk().withdraw()
filename = filedialog.askopenfilename()

import scipy.integrate as integrate
import numpy as np
import cmath
import pandas as pd
from lmfit import Model
import sys

data = pd.read_csv(filename)


def l_r(v, beta, f):
    return (f * (8 - (4 * beta)) / 3) * cmath.exp(
        beta * v) * cmath.exp(-cmath.exp(v))


def integrand(x, omega, tau_c, beta, f):
    return l_r(x, beta, f) / (1 + 1j * omega * (tau_c * cmath.exp(x)))


def re_int(x, omega, tau_c, beta, f):
    try:
        return np.real(integrand(x, omega, tau_c, beta, f))
    except OverflowError:
        return 0


def im_int(x, omega, tau_c, beta, f):
    try:
        return np.imag(integrand(x, omega, tau_c, beta, f))
    except OverflowError:
        return 0


#eta = float(input("Enter eta: "))
kappa = 8.


def function(x, G_inf, beta, f, eta):
    tau_m = eta / G_inf
    tau_c = kappa * tau_m

    re = np.zeros(x.size)
    im = np.zeros(x.size)
    for i in range(0, x.size):
        re[i] = (integrate.quad(
            re_int, -np.inf, +np.inf, args=(x[i], tau_c, beta, f)))[0]
        im[i] = (integrate.quad(
            im_int, -np.inf, +np.inf, args=(x[i], tau_c, beta, f)))[0]

    integral = re + (im * 1j)
    tmp = 1 + integral - (1j / (x * tau_m))
    G_res = G_inf / tmp
    return G_res


X = np.array(data.AF)
YReal = np.array(data.SM / 1e9)
YImag = np.array(data.LM / 1e9)
Y = YReal + YImag * 1j

from matplotlib import pyplot as plt

model = Model(function)
params = model.make_params()
params['G_inf'].set(value=0.8, min=0.1, max=30)
params['beta'].set(value=0.6, min=0.1, max=1)
#params['kappa'].set(value=8, min=1, max=50)
params['eta'].set(value=0.1, min=0, max=100)
params['f'].set(value=0.5, min=0.1, max=2)
print("Fitting...")
result = model.fit(Y, x=X, params=params)
YFit = result.best_fit
print("Complete!", result.best_values)
plt.scatter(X, np.real(Y))
plt.scatter(X, np.imag(Y))
plt.plot(X, np.real(YFit))
plt.plot(X, np.imag(YFit))
plt.yscale('log')
plt.xscale('log')
plt.show()

if len(sys.argv) > 1:
    out = open(str(sys.argv[1]), "w+")
    csv = "Omega,G_Prime,G_Double_Prime\n"
    for i in range(0, X.size):
        csv += f"{float(X[i])},{float(np.real(YFit[i]))},{float(np.imag(YFit[i]))}"
        csv += "\n"
    out.write(csv)
