# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:53:11 2022

@author: Shintaro Nagase (nagase@cns.s.u-tokyo.ac.jp) 
@co-author: Roman Wixinger (roman.wixinger@gmail.com)

MOT constants for the old CCD camera. For constants for the new CMOS camera
check out the corresponding file. 
"""

import numpy as np


# Natural constants
hbar= 1.054571817 * 10**(-34)     # Planck constant (Js)
c = 299792458                     # Speed of light (m/s)

# MOS
Cell_xsize = 3.45 * 10**(-6)      # CCD Cell x size (m) -> TODO: CHECK
Cell_ysize = 3.45 * 10**(-6)      # CCD Cell y size (m) -> TODO: CHECK
T_exp = 50 * 10**(-6)             # Exposure time -> TODO: CHECK
eta = 0.3                         # Quantum efficiency [Rb]
eta_FR = 0.46                     # Quantum efficiency [Fr]
b = 10/5.3277                     # Lens magnification -> TODO: CHECK

# Atom
lambda_Rb = 780 * 10**(-9)          # Fluorescence wavelength (m)
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

# Gaussian model
def two_D_gauss(X: tuple, 
                A: float, 
                sigma_x: float, 
                sigma_y: float, 
                mu_x: float, 
                mu_y: float, 
                C: float): 
    x, y = X 
    z = A * Cell_xsize * Cell_ysize\
        / (2*np.pi*np.sqrt(sigma_x**2*sigma_y**2))\
        * np.exp(-(x-mu_x)**2/(2*sigma_x**2))\
        * np.exp(-(y-mu_y)**2/(2*sigma_y**2))\
        + C

    return z

# Conversion formula [CCD]
Pow_elec_coef =  (T_exp*eta)/(hbar * omega0_Rb)  #  Power (W) → Signal (electron) conversion 
MOTnum_Pow_coef = hbar*omega0_Rb*Gamma_Rb/2 * s_0/(1+s_0) * 1/(1+(2*delta/Eff_Gamma_Rb)**2) * Omega_VP/(4*np.pi)  # MOT Atomic Number to Power (W) Conversion
Elec_MOTnum_coef = 1.0 / MOTnum_Pow_coef  / Pow_elec_coef #  Signal (electron) to MOT number conversion 

# Current integrator
pulse_per_coulomb = 10^-6   # (1/C)

# PMT
Gain = 1.0                  # (1)
beta_cathode = 63.0 / 1000  # (A/W)

# Conversion formula [PMT, Rubidium]
Pow_pulses_per_s_coef = (1.0 / pulse_per_coulomb) * (1.0/(Gain * beta_cathode)) 
MOTnum_pulses_per_s_coef = Pow_pulses_per_s_coef / MOTnum_Pow_coef 

# Conversion formula [PMT, Francium]


# Input data (observed csv data from new CCD camera) 
Xmin = 0            # Region of interest -> 175
Xmax = 504          # Region of interest -> 232
Ymin = 0            # Region of interest -> 233 
Ymax = 504          # Region of interest -> 290
Xnum = Xmax - Xmin
Ynum = Ymax - Ymin



# Functions
def convert_pulse_rate_to_MOT(pulse_rate: float, with_beamsplitter: bool): 
    """ Takes the pulse rate [1/s] of the PMT and whether or not a beamsplitter 
        was applied. Returns the MOT number. 
    """
    return pulse_rate * MOTnum_pulses_per_s_coef * (2.0 if with_beamsplitter else 1.0)
