# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:53:11 2022

@author: roman

MOT constants. 
"""

import numpy as np


hbar= 1.054571817 * 10**(-34)     # Planck constant (Js)
c = 299792458                     # Speed of light (m/s)

# CCD  
Cell_xsize = 6.45 * 10**(-6)      # CCD Cell x size (m)
Cell_ysize = 6.45 * 10**(-6)      # CCD Cell y size (m)
T_exp = 50 * 10**(-6)             # Exposure time
eta = 0.5                         # Quantum efficiency
b = 10/5.3277                     # Lens magnification

# Atom
lambda_Rb = 780 * 10**(-9)        # Fluorescence wavelength (m)
omega0_Rb = 2*np.pi*c/lambda_Rb
Gamma_Rb = 2*np.pi * 7.6 * 10**(6)  # Life span (Hz)
I_sat = 3.5771                      # Saturation strength (mW/cm^2)

# Laser
x_power = 9 *2                      # x-axis optical power (mW) 2x is the return light
y_power = 10 *2
z_power = 9 *2
beam_diam = 1.7                                 # Light beam diameter (cm)
x_intens = x_power/(np.pi*((beam_diam/2)**2))   # z-axis light intensity (mW/cm^2)
y_intens = y_power/(np.pi*((beam_diam/2)**2))
z_intens = z_power/(np.pi*((beam_diam/2)**2))
I_beam = x_intens + y_intens + z_intens         # MOT Central light intensity
s_0 = I_beam / I_sat                            # Saturation parameter
delta = 2*np.pi * 10 * 10**(6)                  # Separation (Hz)
Eff_Gamma_Rb = Gamma_Rb * np.sqrt(1 + s_0)      # Effective line width

# Calculation of solid angle
VP_area = 8**2 * np.pi              # ICF34 viewport area (cm^2)
r_VP = 65                           # Distance from MOT center to viewport (cm)
Omega_VP = VP_area / r_VP**2        # Solid angle of viewport

# Conversion formula
Pow_elec_coef =  (T_exp*eta)/(hbar * omega0_Rb)     # Power (W) → Signal (electron) conversion 
MOTnum_Pow_coef = hbar*omega0_Rb*Gamma_Rb/2 * s_0/(1+s_0) * 1/(1+(2*delta/Eff_Gamma_Rb)**2) * Omega_VP/(4*np.pi)    # MOT原子数→パワー(W)変換

# Input data (observed data)
Xmin = 480
Xmax = 560
Ymin = 630
Ymax = 810
Xnum = Xmax - Xmin
Ynum = Ymax - Ymin
