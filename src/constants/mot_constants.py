# -*- coding: utf-8 -*-
"""MOT constants for the old CCD camera and for the new CMOS camera.

We store the constants in dicts. Note that the region of interest (ROI) can change quite a lot, even during a beamtime.
This is an unsolved problem.

Todo:
    * Check that the constants are set correctly.
    * Solve the problem with the region of interest. Maybe it can be detected automatically.
    * Check the attributes VP_area and r_VP, which might be specific to one setup.
"""

import numpy as np


class CameraConstants(object):
    """ Stores the constants of the setup related to the CMOS camera.

    The class has custom getters for composite attributes, which are calculated from multiple attributes.
    This makes it possible to update attributes without introducing inconsistencies.
    """

    # Universal constants
    hbar = 1.054571817 * 10**(-34)     # Planck constant (Js)
    c = 299792458                      # Speed of light (m/s)

    # Atom
    lambda_Rb = 780 * 1e-9             # Fluorescence wavelength (m)
    omega0_Rb = 2 * np.pi * 299792458
    Gamma_Rb = 2 * np.pi * 7.6 * 1e6     # Life span (Hz)
    I_sat = 3.5771                     # Saturation strength (mW/cm^2)
    
    def __init__(self,
                 Cell_xsize: float,
                 Cell_ysize: float, 
                 T_exp: float,
                 eta: float,
                 x_power: float,
                 y_power: float, 
                 z_power: float,
                 model: callable,
                 pulse_per_coulomb: float,
                 Gain: float,
                 beta_cathode: float,
                 Xmin: int,
                 Xmax: int,
                 Ymin: int, 
                 Ymax: int):

        # Cell
        self.Cell_xsize = Cell_xsize            # CCD Cell x size (m)
        self.Cell_ysize = Cell_ysize            # CCD Cell y size (m)
        self.T_exp = T_exp                      # Exposure time
        self.eta = eta                          # Quantum efficiency
        self.b = eta                            # Lens magnification
        
        # Laser
        self.x_power = x_power                  # x-axis optical power (mW) 2x is the return light
        self.y_power = y_power
        self.z_power = z_power
        self.beam_diam = 1.7                    # Light beam diameter (cm)
        self.delta = 2 * np.pi * 10 * 1e6       # Separation (Hz)

        # Model
        self.model = model

        # Calculation of solid angle
        self.VP_area = 8**2 * np.pi             # ICF34 viewport area (cm^2)
        self.r_VP = 65                          # Distance from MOT center to viewport (cm)

        # Current integrator
        self.pulse_per_coulomb = pulse_per_coulomb  # (1/C)

        # PMT
        self.Gain = Gain                  # (1)
        self.beta_cathode = beta_cathode  # (A/W)

        # Region of interest (ROI)
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Ymin = Ymin
        self.Ymax = Ymax

    # Laser
    @property
    def x_intens(self) -> float:
        """ The x-axis light intensity [mW/cm^2]. """
        return self.x_power/(np.pi*((self.beam_diam/2)**2))

    @property
    def y_intens(self) -> float:
        """ The y-axis light intensity [mW/cm^2]. """
        return self.y_power/(np.pi*((self.beam_diam/2)**2))

    @property
    def z_intens(self) -> float:
        """ The z-axis light intensity [mW/cm^2]. """
        return self.z_power/(np.pi*((self.beam_diam/2)**2))

    @property
    def I_beam(self) -> float:
        """MOT Central light intensity. """
        return self.x_intens + self.y_intens + self.z_intens

    @property
    def s_0(self) -> float:
        """ Saturation parameter. """
        return self.I_beam / self.I_sat

    @property
    def Eff_Gamma_Rb(self):
        """ Effective line width. """
        return self.Gamma_Rb * np.sqrt(1 + self.s_0)

    # Calculation of the solid angle
    @property
    def Omega_VP(self):
        """Solid angle of viewport.
        """
        return self.VP_area / self.r_VP**2

    # Model
    @property
    def two_D_gauss(self):
        return lambda X, A, sigma_x, sigma_y, mu_x, mu_y, C: self.model(
            X, A, sigma_x, sigma_y, mu_x, mu_y, C, self.Cell_xsize, self.Cell_ysize
        )

    # Conversion formula [CCD]
    @property
    def Pow_elec_coef(self):
        """Power (W) → Signal (electron) conversion. """
        return (self.T_exp * self.eta)/(self.hbar * self.omega0_Rb)

    @property
    def MOTnum_Pow_coef(self):
        """MOT Atomic Number to Power (W) conversion. """
        return self.hbar\
               * self.omega0_Rb \
               * self.Gamma_Rb/2 \
               * self.s_0/(1+self.s_0) \
               * 1/(1+(2*self.delta/self.Eff_Gamma_Rb)**2)\
               * self.Omega_VP/(4*np.pi)

    @property
    def Elec_MOTnum_coef(self):
        """Signal (electron) to MOT number conversion. """
        return 1.0 / self.MOTnum_Pow_coef / self.Pow_elec_coef

    # Conversion formula [PMT, Rubidium]
    @property
    def Pow_pulses_per_s_coef(self):
        """Conversion formula.

        Todo:
            * Add description.
        """
        return (1.0 / self.pulse_per_coulomb) * (1.0/(self.Gain * self.beta_cathode))

    @property
    def MOTnum_pulses_per_s_coef(self):
        """Conversion formula.

        Todo:
            * Add description.
        """
        return self.Pow_pulses_per_s_coef / self.MOTnum_Pow_coef

    # Region of interest
    @property
    def Xnum(self):
        """Width of the region of interest (ROI) in pixels.
        """
        return self.Xmax - self.Xmin

    @property
    def Ynum(self):
        """Height of the region of interest (ROI) in pixels.
        """
        return self.Ymax - self.Ymin


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


# Original CCD
c_ccd = CameraConstants(
    Cell_xsize=6.45 * 10**(-6),
    Cell_ysize=6.45 * 10**(-6), 
    T_exp=50 * 10**(-6),
    eta=0.5,
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    model=two_D_gauss,
    pulse_per_coulomb=1e-6,
    Gain=1.0,
    beta_cathode=63.0 / 1000,
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
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    model=two_D_gauss,
    pulse_per_coulomb=1e-6,
    Gain=1.0,
    beta_cathode=63.0 / 1000,
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
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    model=two_D_gauss,
    pulse_per_coulomb=10e-6,
    Gain=1.0,
    beta_cathode=63.0 / 1000,
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
    x_power=9 * 2,
    y_power=10 * 2, 
    z_power=9 * 2,
    model=two_D_gauss,
    pulse_per_coulomb=1e-6,
    Gain=1.0,
    beta_cathode=63.0 / 1000,
    Xmin=850,
    Xmax=950,
    Ymin=300, 
    Ymax=400
)
