import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy import stats
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 参考：https://rikei-fufu.com/2020/07/05/post-3270-fitting/
# メモ：上記サイトにはフィッティングパラメータの初期値を入れていないが、オーダーを合わせた初期値を入れないとうまくフィッティングできない。下記コードには初期値『p0』を入力した。

def fitting_2DGauss(data):
    def two_D_gauss(X, A, sigma_x, sigma_y, mu_x, mu_y, C): # 2D Gaussian
        x, y = X #説明変数(独立変数)を分離する。
        z = (A *Cell_xsize*Cell_ysize / (2*np.pi*np.sqrt(sigma_x**2*sigma_y**2))) * np.exp(-(x-mu_x)**2/(2*sigma_x**2)) * np.exp(-(y-mu_y)**2/(2*sigma_y**2)) + C

        return z

    def plot_fit_result(data, fit_result):
        #グラフの枠を作っていく
        fig = plt.figure()
        ax = Axes3D(fig)

        #描画
        ax.plot(data["x"],data["y"],data["z"], ms=3, marker="o",linestyle='None', c="blue")         #実測データ値は散布図でplot
        ax.plot_wireframe(fit_result["x"],fit_result["y"],fit_result["z"], rstride=10, cstride=10)  #fitting結果は面(ワイヤーフレーム)でplot
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('atom number')
        plt.savefig("Plot.png", dpi=300)        #グラフを画像データで保存
        plt.show(block=False)                                                                       #グラフを表示
        return 0

    x_observed = data["x"]
    y_observed = data["y"]
    z_observed = data["z"]

    p0 = np.array([ 5000./MOTnum_Pow_coef, 50.*Cell_xsize*b, 100*Cell_ysize*b, 525.*Cell_xsize*b, 720.*Cell_ysize*b, 100.])
    #fittingのメイン計算部分
    popt, pcov = curve_fit(two_D_gauss, (x_observed, y_observed), z_observed, p0) #poptは最適推定値、pcovは共分散が出力される
    perr = np.sqrt(np.diag(pcov)) #推定されたパラメータの各々の誤差

    #Chi2 contingency
    o = z_observed #観測データ
    e = two_D_gauss((x_observed, y_observed), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5]) #推定データ
    chi2 = stats.chisquare(o, f_exp = e) #カイ自乗計算のメイン部分。chi2には[カイ二乗, p値]の2つが出力される。

    #R2 calc
    residuals =  o - e #残渣
    rss = np.sum(residuals**2)      #残差平方和: residual sum of squares = rss
    tss = np.sum((o-np.mean(o))**2) #全平方和: total sum of squares = tss
    r_squared = 1 - (rss / tss)     #決定係数R^2

    #fittingの結果をターミナルに表示
    print("*Result************")
    print("z = (A/(2*np.pi*sigma_x*sigma_y)) * np.exp(-(x-mu_x)**2/(2*sigma_x**2)) * np.exp(-(y-mu_y)**2/(2*sigma_y**2)) + C")
    print("A = ", popt[0], "+-", perr[0])
    print("sigma_x = ", popt[1], "+-", perr[1])
    print("sigma_y = ", popt[2], "+-", perr[2])
    print("mu_x = ", popt[3], "+-", perr[3])
    print("mu_y = ", popt[4], "+-", perr[4])
    print("C = ", popt[5], "+-", perr[5])
    print("X-squared = ", chi2[0])
    print("p-value = ", chi2[1])
    print("R^2 = ", r_squared)
    print("s_0 = ",s_0)
    print("*******************")
    statistics_numbers = {  "X-squared": chi2[0],
                            "p-value": chi2[1],
                            "R^2": r_squared}

    #グラフ用に、fittingの結果を示す曲面を作成
    fit_x = np.linspace(min(data["x"]), max(data["x"]), 200)
    fit_y = np.linspace(min(data["y"]), max(data["y"]), 200)
    X, Y = np.meshgrid(fit_x, fit_y)
    fit_z = two_D_gauss((X, Y), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
    fit_result={"x":X, "y":Y, "z":fit_z}

    #グラフでfitting結果を表示
    plot_fit_result(data, fit_result)

    return popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], statistics_numbers

if __name__=="__main__":

    # 物理定数
    
    hbar = 1.054571817 * 10**(-34)  # 換算プランク定数 (Js)
    c = 299792458   # 光速 (m/s)

    # CCDの特性   
    Cell_xsize = 6.45 * 10**(-6)   # CCD Cell x size (m)
    Cell_ysize = 6.45 * 10**(-6)   # CCD Cell y size (m)
    T_exp = 50 * 10**(-6)   # 露光時間
    eta = 0.5   # 量子効率
    b = 10/5.3277   # レンズの倍率

    # 原子
    lambda_Rb = 780 * 10**(-9)  # 蛍光波長 (m)
    omega0_Rb = 2*np.pi*c/lambda_Rb
    Gamma_Rb = 2*np.pi * 7.6 * 10**(6)  # 寿命 (Hz)
    I_sat = 3.5771    # 飽和強度 (mW/cm^2)

    # レーザー
    x_power = 9 *2   # x軸光パワー (mW) 2倍は打ち返し光
    y_power = 10 *2
    z_power = 9 *2
    beam_diam = 1.7  # 光ビーム直径 (cm)
    x_intens = x_power/(np.pi*((beam_diam/2)**2))   # z軸光強度 (mW/cm^2)
    y_intens = y_power/(np.pi*((beam_diam/2)**2))
    z_intens = z_power/(np.pi*((beam_diam/2)**2))
    I_beam = x_intens + y_intens + z_intens     # MOT中心光強度
    s_0 = I_beam / I_sat    # 飽和パラメータ
    delta = 2*np.pi * 10 * 10**(6)  # 離調 (Hz)
    Eff_Gamma_Rb = Gamma_Rb * np.sqrt(1 + s_0)  # 有効線幅

    # 立体角計算
    VP_area = 8**2 * np.pi  # ICF34ビューポートの面積 (cm^2)
    r_VP = 65   # MOT中心からVPまでの距離 (cm)
    Omega_VP = VP_area / r_VP**2    # VPの立体角

    # 変換式
    Pow_elec_coef =  (T_exp*eta)/(hbar * omega0_Rb)     # パワー(W) → シグナル(electron)変換
    MOTnum_Pow_coef = hbar*omega0_Rb*Gamma_Rb/2 * s_0/(1+s_0) * 1/(1+(2*delta/Eff_Gamma_Rb)**2) * Omega_VP/(4*np.pi)    # MOT原子数→パワー(W)変換

    #入力データ(観測データ)
    Xmin = 480
    Xmax = 560
    Ymin = 630
    Ymax = 810
    Xnum = Xmax - Xmin
    Ynum = Ymax - Ymin

    x_data = np.array([np.arange(Xmin,Xmax)]*Ynum).reshape(-1)*Cell_xsize*b
    y_data= np.repeat(np.arange(Ymin,Ymax), Xnum)*Cell_ysize*b

    all_data = pd.read_excel("C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot\\images\\ccd_detuning10.xlsx", index_col=None, header=None)
    data = all_data.iloc[Ymin:Ymax, Xmin:Xmax]
    z_data = data.to_numpy().reshape(-1) / Pow_elec_coef / MOTnum_Pow_coef

    fit_data = {"x": x_data,
                "y": y_data,
                "z": z_data}
#    print(fit_data["x"])

    #fittingを行う関数の読み出し
    A, sigma_x, sigma_y, mu_x, mu_y, B, statistics_numbers = fitting_2DGauss(fit_data)

    #入力待機
    Answer="n"
    while Answer != "y":
        print("Do you want to stop this program? (y/n)")
        Answer = input(">> ")
    print("End")