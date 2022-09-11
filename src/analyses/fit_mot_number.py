# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:37:36 2022

@author: Shintaro Nagase (nagase@cns.s.u-tokyo.ac.jp) 
@co-author: Roman Wixinger (roman.wixinger@gmail.com)

Extraction of the MOT number from SSD images. 

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


def load(url): 
    return pd.read_excel(url, index_col=None, header=None)

def preprocess(df: pd.DataFrame, mode: str): 
    """ Takes the ssd image data as pandas dataframe and converts into 
        numpy arrays. The unit is converted using a scaling factor which is 
        applied to the z values. The scaling factor can be determined from the
        mode, which is either 'power' or 'mot number'. 
    """
    
    x_data = np.array([np.arange(c.Xmin, c.Xmax)] * c.Ynum).reshape(-1) * c.Cell_xsize * c.b
    y_data= np.repeat(np.arange(c.Ymin, c.Ymax), c.Xnum) * c.Cell_ysize * c.b

    data = df.iloc[c.Ymin:c.Ymax, c.Xmin:c.Xmax]
    
    scaling_factor = {
        "power": 1.0 / c.Pow_elec_coef / c.MOTnum_Pow_coef, 
        "mot number": c.hbar * c.omega0_Rb / (c.T_exp * c.eta)
        }[mode]
    
    z_data = data.to_numpy().reshape(-1) * scaling_factor

    data = {
        "x": x_data,
        "y": y_data,
        "z": z_data
        }
    
    return data

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

def fitting(model, data):

    # Extraction
    x = data["x"]
    y = data["y"]
    z = data["z"]

    # Initial guess for fit parameters
    p0 = np.array([5000., 
                   50. * c.Cell_xsize * c.b, 
                   100 * c.Cell_ysize * c.b, 
                   525.*c.Cell_xsize*c.b, 
                   720.*c.Cell_ysize*c.b, 
                   100.])
    
    # Fitting: popt is the best estimate, pcov is the covariance output
    popt, pcov = curve_fit(two_D_gauss, (x, y), z, p0)
    perr = np.sqrt(np.diag(pcov)) # Error for each of the estimated parameters

    # Chi2 contingency
    o = z                                                                           # Observed data
    e = two_D_gauss((x, y), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])   # Estimated data
    e_normalized = e * sum(o) / sum(e)                                              # Normalize estimate such that chi2 estimation works
    chi2 = stats.chisquare(o, f_exp = e_normalized) # Chi2 outputs two [chi-square, p-value].

    # R2 calculation
    residuals =  o - e              # Residual
    rss = np.sum(residuals**2)      # Residual sum of squares = rss
    tss = np.sum((o-np.mean(o))**2) # Total sum of squares = tss
    r_squared = 1 - (rss / tss)     # Coefficient of determination R^2
    
    # Save as dict
    statistics = {
        "X-squared": chi2[0],
        "p-value": chi2[1],
        "R^2": r_squared,
        "popt": popt, 
        "pcov": pcov,
        "perr": perr,
        "chi2": chi2,
        "r_squared": r_squared
        }
    
    return statistics
    
def generate_fit_data(data, statistics: dict): 
    # Extract fit parameters
    popt = statistics["popt"]

    # Create a surface showing the result of fitting for a graph
    fit_x = np.linspace(min(data["x"]), max(data["x"]), 200)
    fit_y = np.linspace(min(data["y"]), max(data["y"]), 200)
    X, Y = np.meshgrid(fit_x, fit_y)
    
    # Evaluate the fitted model on the grid
    fit_z = two_D_gauss((X, Y), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
    
    # Convert the fit into the same format as the data
    fit_data = {"x": X, "y": Y, "z": fit_z}
    return fit_data

def plot_fit_result(data, fit_data, url, mode: str):
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
    plt.savefig(url, dpi=300)
    plt.show(block=False)

def print_stats(statistics: dict):
    
    print(" Result ***********")
    print("z = (A/(2*np.pi*sigma_x*sigma_y)) * np.exp(-(x-mu_x)**2/(2*sigma_x**2)) * np.exp(-(y-mu_y)**2/(2*sigma_y**2)) + C")
    print("A = ", statistics["popt"][0], "+-", statistics["perr"][0])
    print("sigma_x = ", statistics["popt"][1], "+-", statistics["perr"][1])
    print("sigma_y = ", statistics["popt"][2], "+-", statistics["perr"][2])
    print("mu_x = ", statistics["popt"][3], "+-", statistics["perr"][3])
    print("mu_y = ", statistics["popt"][4], "+-", statistics["perr"][4])
    print("C = ", statistics["popt"][5], "+-", statistics["perr"][5])
    print("X-squared = ", statistics["chi2"][0])
    print("p-value = ", statistics["chi2"][1])
    print("R^2 = ", statistics["r_squared"])
    print("*******************")
    

if __name__=="__main__":
    
    # Settings
    mode = "mot number"
    url = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot\\images\\ccd_detuning10.xlsx"
    target = "fit.png"
    
    # Run
    df = load(url=url)
    data = preprocess(df, mode=mode)
    statistics = fitting(model=two_D_gauss, data=data)
    fit_data = generate_fit_data(data, statistics)
    plot_fit_result(data, fit_data, url=target, mode=mode)
    print_stats(statistics)
    
    
    
