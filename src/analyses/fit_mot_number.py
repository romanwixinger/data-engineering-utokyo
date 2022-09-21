# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:37:36 2022

@author: Shintaro Nagase (nagase@cns.s.u-tokyo.ac.jp) 
@co-author: Roman Wixinger (roman.wixinger@gmail.com)

Extraction of the MOT number and power from SSD images. 

Takes dataframes with image data and some references dataframes from the 
same camera with just noise. Estimates the dead pixels and subtracts them
from the images. Performs Maximum Likelihood Estimation (MLE) with a 
2D Gaussian model in the image data and plot a 3D view and a 2D heatmap. 

Sources: 
- https://rikei-fufu.com/2020/07/05/post-3270-fitting/
"""

import sys
sys.path.insert(0,'..')

import os
from datetime import datetime
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy import stats
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import mot_constants as c_ccd
import mot_constants_cmos as c_cmos


# Settings
c = c_ccd


class MOTMLE():
    
    def __init__(self, c, reference_dfs: list[pd.DataFrame]): 
        self.c = c
        self.dead_pixels = None

    def load(self, source: str) -> pd.DataFrame: 
        """ Load the pandas dataframe and the right constants. """
        if ".xlsx" in source: 
            df = pd.read_excel(source, index_col=None, header=None)
        else: 
            df = pd.read_csv(source, index_col=None, header=None)
        return df

    def find_dead_pixels(self): 
        """ TODO: Implement method which takes the reference dfs and finds the 
            pixels which always have the same value. Create a vectorized 
            method which subtract this noise. 
        """
        pass
        
    
    def preprocess(self, df: pd.DataFrame, mode: str): 
        """ Takes the ssd image data as pandas dataframe and converts into 
            numpy arrays. Converts the unit of the z-axis. 
        """
        
        # Create x, y
        x_data = np.array([np.arange(self.c.Xmin, self.c.Xmax)] * self.c.Ynum).reshape(-1) * self.c.Cell_xsize * self.c.b
        y_data= np.repeat(np.arange(self.c.Ymin, self.c.Ymax), self.c.Xnum) * self.c.Cell_ysize * self.c.b
    
        # Scale z
        scaling_factor = self.get_scaling_factor(mode)
        array = df.iloc[self.c.Ymin:self.c.Ymax, self.c.Xmin:self.c.Xmax]
        z_data = array.to_numpy().reshape(-1) * scaling_factor
        
        # Combine
        data = {"x": x_data, "y": y_data, "z": z_data}
        return data
    
    def get_scaling_factor(self, mode: str) -> float: 
        """ The unit of the z axis can be converted using a scaling factor. This 
            function returns the scaling factor, which can be determined from the
            mode, which is either 'power' or 'mot number'. 
        """
        scaling_factor = {
            "mot number": 1.0 / self.c.Pow_elec_coef / self.c.MOTnum_Pow_coef, 
            "power": self.c.hbar * self.c.omega0_Rb / (self.c.T_exp * self.c.eta)
            }[mode]
        return scaling_factor
    
    def fitting(self, model: callable, data: dict, mode: str):
        """ Fit the model to the data."""
    
        # Extraction
        x, y, z = data["x"], data["y"], data["z"]
    
        # Initial guess for fit parameters
        p0 = self.get_initial_guess(data, mode)
        
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
        return self.extract_statistics(r_squared, chi2, popt, pcov, perr)
    
    def extract_statistics(self, r_squared, chi2, popt, pcov, perr): 
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
        
    def get_initial_guess(self, data: dict, mode: str): 
        """ Proposes initial guesses for the fitting parameters with heuristics. 
        """
        x, y, z = data["x"], data["y"], data["z"] 
        
        # Give data points that are 2 sigma above average a high weight
        mean_z = np.mean(z)
        std_z = np.std(z)
        only_peak = lambda x: 1.0 if x > mean_z + 2*std_z else 1e-9
        pick_only_peak = np.vectorize(only_peak)
        weights = pick_only_peak(z) 
        
        A = 6e5 if mode == "mot number" else 1e-6
        mu_x = np.average(x, weights=weights)
        mu_y = np.average(y, weights=weights)
        sigma_x = np.sqrt(np.average((x - mu_x)**2, weights=weights))
        sigma_y = np.sqrt(np.average((y - mu_y)**2, weights=weights))
        
        print("mu_x =", mu_x, "mean x =", np.mean(x))
        print("mu_y =", mu_y, "mean y =", np.mean(y))
        print("sigma_x =", sigma_x, "std_x =", np.std(x))
        print("sigma_y =", sigma_y, "std_y =", np.std(y))
        
        C = 1e2 if mode == "mot number" else 1e-12
        p0 = np.array([A, sigma_x, sigma_y, mu_x, mu_y, C])
        return p0
        
    def generate_fit_data(self, model: callable, data: dict, statistics: dict): 
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
        fit_z = model((X, Y), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
        # fit_z = two_D_gauss((X, Y), 200000., 0.0001, 0.0001, 0.00624, 0.0091, 102.)
        
        # Convert the fit into the same format as the data
        fit_data = {"x": X, "y": Y, "z": fit_z}
        return fit_data
    
    def plot_fit_result(self, data: dict, fit_data: dict, target: str, mode: str, time: str):
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
    
        # Plot fitted data       
        if fit_data is not None: 
            ax.plot_wireframe(fit_data["x"], 
                              fit_data["y"], 
                              fit_data["z"], 
                              rstride=10, 
                              cstride=10)
            
        # Labels
        ax.set_title(f"Image recorded at {time}")
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Power (W)' if mode=="power" else 'Atom number [1/pixel]')
        
        # Save image
        plt.savefig(target, dpi=300)
        plt.show(block=False)
        
    def plot_heatmap(self, data: dict, fit_data, target: str, mode: str, time: str):
        """ Plots the 3d data and the fit. Saves the image to the url. 
        """
        
        # Setup figure
        z = data["z"]
        z_arr = z.reshape((self.c.Ynum, self.c.Xnum))
        
        if fit_data is None: 
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 3),
                            subplot_kw={'xticks': [], 'yticks': []})
    
            ax.imshow(z_arr, cmap='hot', interpolation='nearest')
            ax.set_title("Camera signal")
        else: 
            z_fit = fit_data["z"]
            z_arr_fit = z_fit.reshape((200, 200))
            fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 6),
                            subplot_kw={'xticks': [], 'yticks': []})
            
            for ax, arr, title in zip(axs, [z_arr, z_arr_fit], ["Camera signal", "Fit"]): 
                ax.imshow(arr, cmap='hot', interpolation='nearest')
                ax.set_title(title)
    
        plt.tight_layout()
        plt.savefig(target, dpi=300)
        plt.show()   
        
    def time(self, source: str): 
        """ Return the time when the file was created. 
        """
        
        timestamp = os.path.getctime(source)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    def print_stats(self, statistics: dict):
        if not statistics["fit_successful"]: 
            print(" Result ***********")
            print("Fit was not succesful.")
            print("*******************")
            return
            
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
        
    def perform_analysis(self, source: str, target: str, mode: str, min_signal: int=0): 
        """ Loads the image data, fits a 2D gaussian model on it, generates a plot
            of the original data and a fit, saves the plot, and returns the 
            statistics of the fit. 
            Source is the filepath of the original data and target is the filepath 
            of the plot. The mode can be either 'power' or 'mot number'. 
            If the total sum of the df is less than min_signal, then we 
            terminate the analysis. 
        """
        # Load data
        df = self.load(source=source)
        
        # Check if the image is promising
        total_sum = df.sum().sum() 
        if total_sum < min_signal: 
            print(f"The image was discarded because the total signal is {total_sum} < {min_signal}.")
            return {
                "fit_successful": False, 
                "total_sum": total_sum, 
                "enough_pulses": False,
                }
        print(f"The image will be analyzed, the total signal is {total_sum} > {min_signal}.")
            
        # Fit MLE
        data = self.preprocess(df, mode=mode)
        statistics = self.fitting(model=self.c.two_D_gauss, data=data, mode=mode)
        statistics["total_sum"] = total_sum
        statistics["enough_pulses"] = True
        
        # Plot 3D
        time = self.time(source)
        fit_data = self.generate_fit_data(self.c.two_D_gauss, data, statistics)\
            if statistics["fit_successful"] else None
        self.plot_fit_result(data, fit_data, target=target, mode=mode, time=time)
        
        # Plot heatmap
        heatmap_target = target[:-4] + "_heatmap" + target[-4:] 
        self.plot_heatmap(data, fit_data, target=heatmap_target, mode=mode, time=time)

        # Print and return statistics
        self.print_stats(statistics)
        return statistics
    
    
""" Default instance """

mot_mle = MOTMLE(c=c)
perform_analysis = mot_mle.perform_analysis
    

if __name__=="__main__":
    
    for i in list(range(1, 10)): 
        for mode in ["mot number"]: 
            source = f"C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot\\images\\ccd_detuning0{i}.xlsx"
            target = f"fit_{mode}_{i}.png"
            perform_analysis(source, target, mode)
      


