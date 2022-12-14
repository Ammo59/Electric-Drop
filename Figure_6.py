# -*- coding: utf-8 -*-
"""
Spyder Editor
Eletric Drop Project
Figure 6
4/21/2022, edit 5/14/2022
Aramis Kelkelyan
"""

import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

fig1 = plt.figure(1, figsize=(3.5,5))

mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times'
mpl.rcParams['axes.titlesize'] = 16

#define variables
Voltage = [0, 2, 4, 6, 8] #in kV
d_pixels = [238.667, 224, 257, 255.508, 276] #pixels of drop diameter, corresponding to voltage
d = np.multiply(d_pixels, 3.25*10**(-3)/237) #m, diameter of drop
Volume = 1/6*math.pi*d**(3) #m^3
d_electrode2substrate = 11*10**(-3) #vertical distance from electrode plate to substrate

#Electrostatic Force
epsilon = 80.103*8.85*10**(-12) #permittivity of fluid
E = np.divide(np.multiply(Voltage, 1000), d_electrode2substrate)
#E = np.array([0, 181818.18, 363636.36, 545454.54, 727272.72])
qv = 0 #ideal assumption
rho = 998 #kg/m^3, at 20 deg celsius

#use gradient for epsilon
grad_epsilon = np.gradient(epsilon)

if grad_epsilon == []:
    grad_epsilon = 0

#Momentum Force
m = rho*Volume #kg, mass of drop
Vf, Vi = 0.867, 0.2602 #m/s
delta_t = np.multiply([12.857, 12.837, 12.857, 12.286, 12.714],10**(-3)) #far more reasonable results
#delta_t = np.multiply([7.14, 6.45, 8, 5.33, 10],10**(-4)) #seconds
        #all values, except for the first are arbitrary
        #perhaps look at frames for each drop and calculate time difference? 

#Capillary Force
Ri = d/2
Rj = d/2 #change values later
R = 2*Ri*Rj/(Ri+Rj)
theta = np.deg2rad(45) #radians, find value
gamma = 72 * 10**(-3) #liquid surface tension, N/m, update as neccesary
Vol_crit = Volume/(R**3)
a = 8/237 #arbitrary value based on pixels, will be changed
S = a/(2*np.sqrt(Volume/R))

f1_1 = (-0.44507 + 0.050832*theta - 1.1466*theta**2)
f1_2 = (-0.1119 - 0.000411*theta - 0.1490*theta**2)*np.log(Vol_crit)
f1_3 = (-0.012101 - 0.0036456*theta - 0.01255*theta**2)*(np.log(Vol_crit))**2
f1_4 = (-0.0005 - 0.0003505*theta - 0.00029076*theta**2)*(np.log(Vol_crit))**3
f1 = sum([f1_1,f1_2,f1_3,f1_4])

f2_1 = (1.9222 - 0.57473*theta - 1.2918*theta**2)
f2_2 = (-0.0668 - 0.1201*theta - 0.22574*theta**2)*np.log(Vol_crit)
f2_3 = (-0.0013375 - 0.0068988*theta - 0.01137*theta**2)*(np.log(Vol_crit))**2
f2 = sum([f2_1,f2_2,f2_3])

f3_1 = (1.268 - 0.01396*theta - 0.23566*theta**2)
f3_2 = (0.198 + 0.092*theta - 0.06418*theta**2)*np.log(Vol_crit) 
f3_3 = (0.02232 + 0.02238*theta - 0.009853*theta**2)*(np.log(Vol_crit))**2
f3_4 = (0.0008585 + 0.001318*theta - 0.00053*theta**2)*(np.log(Vol_crit))**3
f3 = sum([f3_1,f3_2,f3_3,f3_4])

f4_1 = (-0.010703 + 0.073776*theta - 0.34742*theta**2)
f4_2 = (0.03345 + 0.04543*theta - 0.09056*theta**2)*np.log(Vol_crit)
f4_3 = (0.0018574 + 0.004456*theta - 0.006257*theta**2)*(np.log(Vol_crit))**2
f4 = sum([f4_1,f4_2,f4_3])

#define Forces
Fe = [-1/2*np.multiply(E,E)*epsilon] #needs to be *grad_epsilon 
#Fe = [0.00005, 0.0001, 0.00015, 0.002, 0.0025] #values based on thesis, assumed
    #note that this is an assumption, formula will need to be changed for higher accuracy
    #Fe = 0 at this stage because gradient of a constant = 0

Fm = m*(Vf-Vi)/delta_t

Fg = 4/3*math.pi*rho*9.81*(d/2)**3
#the only way Fg varies with voltage is the diameter of the drop

Fc = -2*math.pi*R*gamma**(f1-f2**(f3*np.log(S) + f4*np.log(S)))
#Fc = 2*math.pi*R*gamma*math.cos(theta); secondary method, not as accurate

Fnet = Fe + Fm - Fc - Fg

#plot
fig, ax = plt.figure(), plt.axes()

plt.plot(Voltage, np.transpose(Fe), lw=2.0)
plt.plot(Voltage, np.transpose(Fm), lw=2.0)
plt.plot(Voltage, np.transpose(Fg), lw=2.0)
plt.plot(Voltage, np.transpose(Fc), lw=2.0)
plt.plot(Voltage, np.transpose(Fnet), lw=2.0)

ax.set(xlim=(0, 8), xticks=np.arange(1,8),
       ylim=(0, 0.005), yticks=np.arange(-0.002, 0.005, 0.0005))

plt.xlabel('Voltage (kV)')
plt.ylabel('Force (N)')
plt.title('Various Forces vs. Applied Voltage')

location = 0 # For the best location
legend_drawn_flag = True
plt.legend(["$F_{E}$", "$F_{M}$" , "$F_{G}$", "$F_{C}$", "$F_{Net}$"], 
           loc=0, frameon=legend_drawn_flag)

fig.show()
