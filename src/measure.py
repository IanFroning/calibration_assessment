import numpy as np
from scipy.optimize import curve_fit # type: ignore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections.abc import Callable
import fit_functions

def voltages_by_angle(get_measurement: Callable[[float], float]) -> list[tuple[float, float]]:
    """
    Calls get_measurement to get a set of voltage measurements by changing the angle.
    Returns a data set that is not intended to be used on its own, but instead as an
    input for the rest of the functions in this module.

    Attempts make the smallest number of measurements that will measure the peak
    voltage, with the following assumptions:
    1. The measured signal has the form of a Gaussian
    2. The angle varies between 0 and 360 degrees, with mean voltage anywhere in that
        range
    3. The distribution's standard deviation is between 4 and 10
    4. The distribution's amplitude is between 10 and 100 V
    5. The distribution's baseline is between 0 and 10 V.
    """
    MAX_SEARCH_ANGLE = 360
    PEAK_FOUND_THRESHOLD = 40
    ANGLE_STEP = 30
    PEAK_SEARCH_RADIUS = 30
    PEAK_STEP_SIZE = 10

    def search_near(angle):
        return [(angle, get_measurement(angle)) for angle in range(
            angle - PEAK_SEARCH_RADIUS, angle + PEAK_SEARCH_RADIUS, PEAK_STEP_SIZE)]

    measurements: list[tuple[float, float]] = []
    for angle in range(0, 360, ANGLE_STEP):
        trial_point = (angle, get_measurement(angle))
        if trial_point[1] > PEAK_FOUND_THRESHOLD:
            return measurements + search_near(angle)
        else:
            measurements.append(trial_point)

    return measurements

def max_voltage(voltages_by_angle: list[tuple[float, float]]) -> float:
    return max(voltages_by_angle, key=lambda m: m[1])[1]

def max_voltage_angle(voltages_by_angle: list[tuple[float, float]]) -> float:
    return max(voltages_by_angle, key=lambda m: m[1])[0]

def measurement_count(voltages_by_angle: list[tuple[float, float]]) -> int:
    return len(voltages_by_angle)

def expected_max_voltage_from_gaussian_fit(voltages_by_angle: list[tuple[float, float]]) -> float:
    return _gaussian_fit(voltages_by_angle)(max_voltage_angle(voltages_by_angle))

def plot_with_gaussian_fit(voltages_by_angle: list[tuple[float, float]]) -> None:
    dataframe = pd.DataFrame.from_records(voltages_by_angle, columns=['angle', 'voltage'])
    sns.relplot(
        data=dataframe,
        x='angle', y='voltage')

    fit_function = _gaussian_fit(voltages_by_angle)
    x_fit = np.linspace(0, 360, 100)
    y_fit = [fit_function(x) for x in x_fit]
    sns.lineplot(x=x_fit, y=y_fit, color='r')
    plt.show()

def _gaussian_fit(voltages_by_angle: list[tuple[float, float]]) -> Callable[[float], float]:
    parameter_values, parameter_covariances = curve_fit(
        fit_functions.gaussian,
        _angles_tried(voltages_by_angle),
        _voltages_measured(voltages_by_angle),
        p0=[max_voltage_angle(voltages_by_angle), 10, 0, 100],
        bounds=(0, [360, np.inf, 100, 100]))
    return lambda angle: fit_functions.gaussian(angle, *parameter_values)

def _angles_tried(voltages_by_angle: list[tuple[float, float]]) -> list[float]:
    return [m[0] for m in voltages_by_angle]

def _voltages_measured(voltages_by_angle: list[tuple[float, float]]) -> list[float]:
    return [m[1] for m in voltages_by_angle]
