import numpy as np

def gaussian(x: float, mu: int, sigma: int, baseline: float, amplitude: int) -> float:
    exponent = (-1 * (((x - mu) / sigma) ** 2)) / 2
    return baseline + (amplitude - baseline) * np.exp(exponent)

