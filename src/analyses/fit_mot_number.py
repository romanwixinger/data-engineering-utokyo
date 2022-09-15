# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:37:36 2022

@author: Shintaro Nagase (nagase@cns.s.u-tokyo.ac.jp) 
@co-author: Roman Wixinger (roman.wixinger@gmail.com)

Extraction of the MOT number and power from SSD images. 

Sources: 
- https://rikei-fufu.com/2020/07/05/post-3270-fitting/
"""

import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy import stats
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import mot_constants as c


def load(source: str) -> pd.DataFrame: 
    return pd.read_excel(source, index_col=None, header=None)

def preprocess(df: pd.DataFrame, mode: str): 
    """ Takes the ssd image data as pandas dataframe and converts into 
        numpy arrays. Converts the unit of the z-axis. 
    """
    
    # Reshape x, y
    x_data = np.array([np.arange(c.Xmin, c.Xmax)] * c.Ynum).reshape(-1) * c.Cell_xsize * c.b
    y_data= np.repeat(np.arange(c.Ymin, c.Ymax), c.Xnum) * c.Cell_ysize * c.b

    # Scale z
    scaling_factor = get_scaling_factor(mode)
    array = df.iloc[c.Ymin:c.Ymax, c.Xmin:c.Xmax]
    z_data = array.to_numpy().reshape(-1) * scaling_factor
    
    # Combine
    data = {"x": x_data, "y": y_data, "z": z_data}
    return data

def get_scaling_factor(mode: str) -> float: 
    """ The unit of the z axis can be converted using a scaling factor. This 
        function returns the scaling factor, which can be determined from the
        mode, which is either 'power' or 'mot number'. 
    """
    scaling_factor = {
        "power": 1.0 / c.Pow_elec_coef / c.MOTnum_Pow_coef, 
        "mot number": c.hbar * c.omega0_Rb / (c.T_exp * c.eta)
        }[mode]
    return scaling_factor

def two_D_gauss(X: tuple, 
                A: float, 
                sigma_x: float, 
                sigma_y: float, 
                mu_x: float, 
                mu_y: float, 
                C: float): 
    x, y = X 
    z = A * c.Cell_xsize * c.Cell_ysize\
        / (2*np.pi*np.sqrt(sigma_x**2*sigma_y**2))\
        * np.exp(-(x-mu_x)**2/(2*sigma_x**2))\
        * np.exp(-(y-mu_y)**2/(2*sigma_y**2))\
        + C

    return z

def fitting(model: callable, data: dict, mode: str):
    """ Fit the model to the data."""

    # Extraction
    x, y, z = data["x"], data["y"], data["z"]

    # Initial guess for fit parameters
    p0 = get_initial_guess(data, mode)
    
    # Fitting: popt is the best estimate, pcov is the covariance output
    try: 
        popt, pcov = curve_fit(model, (x, y), z, p0)
        perr = np.sqrt(np.diag(pcov)) # Error for each of the estimated parameters
    except RuntimeError as e: 
        print(f"RuntimeError in fit: {e}")
        return {"fit_successful": False}
        
    # Chi2 contingency
    o = z                                                                           # Observed data
    e = model((x, y), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])         # Estimated data
    e_normalized = e * sum(o) / sum(e)                                              # Normalize estimate such that chi2 estimation works
    chi2 = stats.chisquare(o, f_exp = e_normalized) # Chi2 outputs two [chi-square, p-value].

    # R2 calculation
    residuals =  o - e              # Residual
    rss = np.sum(residuals**2)      # Residual sum of squares = rss
    tss = np.sum((o-np.mean(o))**2) # Total sum of squares = tss
    r_squared = 1 - (rss / tss)     # Coefficient of determination R^2
    
    # Return statistics
    return extract_statistics(r_squared, chi2, popt, pcov, perr)

def extract_statistics(r_squared, chi2, popt, pcov, perr): 
    return {
        "A": popt[0],
        "A_unc": perr[0],
        "sigma_x": popt[1],
        "sigma_x_unc": perr[1],
        "sigma_y": popt[2],
        "sigma_y_unc": perr[2],
        "mu_x": popt[3],
        "mu_x_unc": perr[3],
        "mu_y": popt[4],
        "mu_y_unc": perr[4],
        "C": popt[5],
        "C_unc": perr[5],
        "R^2": r_squared,
        "X-squared": chi2[0],
        "p-value": chi2[1],
        "popt": popt, 
        "pcov": pcov,
        "perr": perr,
        "chi2": chi2,
        "fit_successful": True
        }
    
def get_initial_guess(data: dict, mode: str): 
    """ Proposes initial guesses for the fitting parameters with heuristics. 
    """
    x, y = data["x"], data["y"] 
    
    A = 6e5 if mode == "power" else 1e-6
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    sigma_x = np.std(x - mu_x * np.ones_like(x))
    sigma_y = np.std(y - mu_y * np.ones_like(y))
    C = 1e2 if mode == "power" else 1e-12
    p0 = np.array([A, sigma_x, sigma_y, mu_x, mu_y, C])
    return p0
    
def generate_fit_data(data: dict, statistics: dict): 
    """ Takes the x, y values of the data and the fit parameter, and returns
        fitted z values on a x, y grid in the same format as the data. 
    """
    # Extract fit parameters
    popt = statistics["popt"]

    # Create a surface showing the result of fitting for a graph
    fit_x = np.linspace(min(data["x"]), max(data["x"]), 200)
    fit_y = np.linspace(min(data["y"]), max(data["y"]), 200)
    X, Y = np.meshgrid(fit_x, fit_y)
    
    # Evaluate the fitted model on the grid
    fit_z = two_D_gauss((X, Y), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
    # fit_z = two_D_gauss((X, Y), 200000., 0.0001, 0.0001, 0.00624, 0.0091, 102.)
    
    # Convert the fit into the same format as the data
    fit_data = {"x": X, "y": Y, "z": fit_z}
    return fit_data

def plot_fit_result(data: dict, fit_data: dict, target: str, mode: str):
    """ Plots the 3d data and the fit. Saves the image to the url. 
    """
    # Setup figure
    fig = plt.figure()
    ax = Axes3D(fig)
    
    # Plot measured data 
    ax.plot(data["x"], 
            data["y"], 
            data["z"], 
            ms=3, 
            marker="o",
            linestyle='None', 
            c="blue")   

    # FPlot fitted data       
    ax.plot_wireframe(fit_data["x"], 
                      fit_data["y"], 
                      fit_data["z"], 
                      rstride=10, 
                      cstride=10)
        
    # Labels
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Power (W)' if mode=="power" else 'atom number')
    
    # Save image
    plt.savefig(target, dpi=300)
    plt.show(block=False)

def print_stats(statistics: dict):
    print(" Result ***********")
    print("z = (A/(2*np.pi*sigma_x*sigma_y)) * np.exp(-(x-mu_x)**2/(2*sigma_x**2)) * np.exp(-(y-mu_y)**2/(2*sigma_y**2)) + C")
    print("A = ", statistics["A"], "+-", statistics["A_unc"])
    print("sigma_x = ", statistics["sigma_x"], "+-", statistics["sigma_x_unc"])
    print("sigma_y = ", statistics["sigma_y"], "+-", statistics["sigma_y_unc"])
    print("mu_x = ", statistics["mu_x"], "+-", statistics["mu_x_unc"])
    print("mu_y = ", statistics["mu_y"], "+-", statistics["mu_y_unc"])
    print("C = ", statistics["C"], "+-", statistics["C_unc"])
    print("X-squared = ", statistics["X-squared"])
    print("p-value = ", statistics["p-value"])
    print("R^2 = ", statistics["R^2"])
    print("*******************")
    
def perform_analysis(source: str, target: str, mode: str): 
    """ Loads the image data, fits a 2D gaussian model on it, generates a plot
        of the original data and a fit, saves the plot, and returns the 
        statistics of the fit. 
        Source is the filepath of the original data and target is the filepath 
        of the plot. The mode can be either 'power' or 'mot number'
    """
    df = load(source=source)
    data = preprocess(df, mode=mode)
    statistics = fitting(model=two_D_gauss, data=data, mode=mode)
    if statistics["fit_successful"]: 
        fit_data = generate_fit_data(data, statistics)
        plot_fit_result(data, fit_data, target=target, mode=mode)
    return statistics
    

if __name__=="__main__":
    
    for i in list(range(1, 10)): 
        for mode in ["mot number", "power"]: 
            source = f"C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot\\images\\ccd_detuning0{i}.xlsx"
            target = f"fit_{mode}_{i}.png"
            perform_analysis(source, target, mode)
            
            
    
