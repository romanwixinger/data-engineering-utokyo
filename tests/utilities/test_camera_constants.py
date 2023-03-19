import pytest

from src.utilities.camera_constants import CameraConstants


standard_args = {
    "Cell_xsize":6.45 * 1e-6,
    "Cell_ysize": 6.45 * 1e-6,
    "T_exp": 50 * 1e-6,
    "eta": 0.5,
    "x_power": 9 * 2,
    "y_power": 10 * 2,
    "z_power": 9 * 2,
    "model": lambda: 0,
    "pulse_per_coulomb": 1e-6,
    "Gain": 1.0,
    "beta_cathode": 63.0 / 1000,
    "Xmin": 480,
    "Xmax": 560,
    "Ymin": 630,
    "Ymax": 810
}


def test_camera_constants_init():
    c = CameraConstants(**standard_args)


def test_camera_constants_Xnum_and_Ynum():
    c = CameraConstants(**standard_args)
    Xnum_expected = standard_args["Xmax"] - standard_args["Xmin"]
    Ynum_expected = standard_args["Ymax"] - standard_args["Ymin"]
    assert Xnum_expected == pytest.approx(c.Xnum), f"Expected {Xnum_expected} but found {c.Xnum} for c.Xnum."
    assert Ynum_expected == pytest.approx(c.Ynum), f"Expected {Ynum_expected} but found {c.Ynum} for c.Ynum."


@pytest.mark.parametrize(["Xnum", "Ynum"], [(0,0), (1,0), (0,1), (1,1)])
def test_camera_constants_update_attributes(Xnum, Ynum):
    c = CameraConstants(**standard_args)

    # Update attributes to different values
    c.Xmin = 10
    c.Xmax = 10 + Xnum
    c.Ymin = 20
    c.Ymax = 20 + Ynum

    assert Xnum == pytest.approx(c.Xnum), f"Expected {Xnum} but found {c.Xnum} for c.Xnum after update."
    assert Ynum == pytest.approx(c.Ynum), f"Expected {Ynum} but found {c.Ynum} for c.Ynum after update."

