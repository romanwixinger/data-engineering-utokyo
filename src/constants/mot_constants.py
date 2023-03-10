# -*- coding: utf-8 -*-
"""MOT constants for the old CCD camera and for the new CMOS camera.

We store the constants in dicts. Note that the region of interest (ROI) can change quite a lot, even during a beamtime.
This is an unsolved problem.

Todo:
    * Check that the constants are set correctly.
    * Solve the problem with the region of interest. Maybe it can be detected automatically.
"""

import numpy as np


class CameraConstants(object):
    
    def __init__(self,
                 Cell_xsize: float,
                 Cell_ysize: float, 
                 T_exp: float,
                 eta: float, 
                 b: float, 
                 x_power: float,
                 y_power: float, 
                 z_power: float,
                 beam_diam: float,
                 delta: float,
                 VP_area: float,
                 r_VP: float,
                 two_D_gauss: callable,
                 pulse_per_coulomb: float,
                 Gain: float,
                 beta_cathode: float,
                 Xmin: int,
                 Xmax: int,
                 Ymin: int, 
                 Ymax: int): 
        # Universal constants
        self.hbar = 1.054571817 * 10**(-34)     # Planck constant (Js)
        self.c = 299792458                      # Speed of light (m/s)
        
        # Atom
        self.lambda_Rb = 780 * 10**(-9)         # Fluorescence wavelength (m)
        self.omega0_Rb = 2*np.pi*self.c
        self.Gamma_Rb = 2*np.pi * 7.6 * 10**(6) # Life span (Hz)
        self.I_sat = 3.5771                     # Saturation strength (mW/cm^2)
        
        self.Cell_xsize = Cell_xsize            # CCD Cell x size (m)
        self.Cell_ysize = Cell_ysize            # CCD Cell y size (m)
        self.T_exp = T_exp                      # Exposure time
        self.eta = eta                          # Quantum efficiency
        self.b = eta                            # Lens magnification
        
        # Laser
        self.x_power = x_power                  # x-axis optical power (mW) 2x is the return light
        self.y_power = y_power
        self.z_power = z_power
        self.beam_diam = 1.7                                            # Light beam diameter (cm)
        self.x_intens = self.x_power/(np.pi*((self.beam_diam/2)**2))    # z-axis light intensity (mW/cm^2)
        self.y_intens = self.y_power/(np.pi*((self.beam_diam/2)**2))
        self.z_intens = self.z_power/(np.pi*((self.beam_diam/2)**2))
        self.I_beam = self.x_intens + self.y_intens + self.z_intens     # MOT Central light intensity
        self.s_0 = self.I_beam / self.I_sat                             # Saturation parameter
        self.delta = 2 * np.pi * 10 * 10**(6)                           # Separation (Hz)
        self.Eff_Gamma_Rb = self.Gamma_Rb * np.sqrt(1 + self.s_0)       # Effective line width
        
        # Calculation of solid angle
        self.VP_area = 8**2 * np.pi                          # ICF34 viewport area (cm^2)
        self.r_VP = 65                                       # Distance from MOT center to viewport (cm)
        self.Omega_VP = self.VP_area / self.r_VP**2          # Solid angle of viewport
        
        # Model
        self.two_D_gauss = lambda X, A, sigma_x, sigma_y, mu_x, mu_y, C: two_D_gauss(
            X, A, sigma_x, sigma_y, mu_x, mu_y, C, self.Cell_xsize, self.Cell_ysize
        )
        
        # Conversion formula [CCD]
        self.Pow_elec_coef =  (self.T_exp * self.eta)/(self.hbar * self.omega0_Rb)  #  Power (W) → Signal (electron) conversion 
        self.MOTnum_Pow_coef = self.hbar*self.omega0_Rb * self.Gamma_Rb/2 * self.s_0/(1+self.s_0) * 1/(1+(2*self.delta/self.Eff_Gamma_Rb)**2) * self.Omega_VP/(4*np.pi)  # MOT Atomic Number to Power (W) Conversion
        self.Elec_MOTnum_coef = 1.0 / self.MOTnum_Pow_coef  / self.Pow_elec_coef    #  Signal (electron) to MOT number conversion 

        # Current integrator
        self.pulse_per_coulomb = pulse_per_coulomb   # (1/C)

        # PMT
        self.Gain = Gain                  # (1)
        self.beta_cathode = beta_cathode  # (A/W)

        # Conversion formula [PMT, Rubidium]
        self.Pow_pulses_per_s_coef = (1.0 / self.pulse_per_coulomb) * (1.0/(self.Gain * self.beta_cathode)) 
        self.MOTnum_pulses_per_s_coef = self.Pow_pulses_per_s_coef / self.MOTnum_Pow_coef 

        # Region of interest (ROI)
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Ymin = Ymin
        self.Ymax = Ymax
        self.Xnum = self.Xmax - self.Xmin
        self.Ynum = self.Ymax - self.Ymin
        
        
def two_D_gauss(X: tuple, 
                A: float, 
                sigma_x: float, 
                sigma_y: float, 
                mu_x: float, 
                mu_y: float, 
                C: float,
                Cell_xsize: float, 
                Cell_ysize: float): 
    x, y = X 
    z = A * Cell_xsize * Cell_ysize\
        / (2*np.pi*np.sqrt(sigma_x**2*sigma_y**2))\
        * np.exp(-(x-mu_x)**2/(2*sigma_x**2))\
        * np.exp(-(y-mu_y)**2/(2*sigma_y**2))\
        + C

    return z


""" Instances """

# Original CCD
c_ccd = CameraConstants(
    Cell_xsize=6.45 * 10**(-6),
    Cell_ysize=6.45 * 10**(-6), 
    T_exp = 50 * 10**(-6),
    eta = 0.5,
    b = 10/5.3277,
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    beam_diam=1.7, 
    delta=2*np.pi * 10 * 10**(6),  
    VP_area=8**2 * np.pi, 
    r_VP=65,
    two_D_gauss=two_D_gauss,
    pulse_per_coulomb=10^-6,
    Gain=1.0,
    beta_cathode = 63.0 / 1000,
    Xmin=480,
    Xmax=560,
    Ymin=630, 
    Ymax=810
    )


# CMOS for beamtime (20220918)
# TODO: Check constants like VP_area and r_VP
c_cmos_Rb_20220918 = CameraConstants(
    Cell_xsize=3.45 * 10**(-6),
    Cell_ysize=3.45 * 10**(-6), 
    T_exp=50 * 10**(-6),
    eta=0.3,
    b=10/5.3277,
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    beam_diam=1.7, 
    delta=2*np.pi * 10 * 10**(6),  
    VP_area=8**2 * np.pi, 
    r_VP=65,
    two_D_gauss=two_D_gauss,
    pulse_per_coulomb=10^-6,
    Gain=1.0,
    beta_cathode = 63.0 / 1000,
    Xmin=175,
    Xmax=232,
    Ymin=233, 
    Ymax=290
    )

# CMOS for beamtime (20220918)
# TODO: Check constants like VP_area and r_VP
c_cmos_Fr_20220918 = CameraConstants(
    Cell_xsize=3.45 * 10**(-6),
    Cell_ysize=3.45 * 10**(-6), 
    T_exp=50 * 10**(-6),
    eta=0.46,
    b=10/5.3277,
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    beam_diam=1.7, 
    delta=2*np.pi * 10 * 10**(6),  
    VP_area=8**2 * np.pi, 
    r_VP=65,
    two_D_gauss=two_D_gauss,
    pulse_per_coulomb=10^-6,
    Gain=1.0,
    beta_cathode = 63.0 / 1000,
    Xmin=175,
    Xmax=232,
    Ymin=233, 
    Ymax=290
    )



# CMOS for laser room
# TODO: Check constants like VP_area and r_VP
c_cmos_laser_room = CameraConstants(
    Cell_xsize=3.45 * 10**(-6),
    Cell_ysize=3.45 * 10**(-6), 
    T_exp = 50 * 10**(-6),
    eta = 0.3,
    b = 10/5.3277,
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    beam_diam=1.7, 
    delta=2*np.pi * 10 * 10**(6),  
    VP_area=8**2 * np.pi, 
    r_VP=65,
    two_D_gauss=two_D_gauss,
    pulse_per_coulomb=10^-6,
    Gain=1.0,
    beta_cathode = 63.0 / 1000,
    Xmin=850,
    Xmax=950,
    Ymin=300, 
    Ymax=400
    )
