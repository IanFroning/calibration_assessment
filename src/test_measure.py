import unittest
import measure
import fit_functions

class TestMeasure(unittest.TestCase):

    gaussian_params = [
        {'mu':180, 'sigma':10, 'baseline':0,  'amplitude':100},
        {'mu':180, 'sigma':10, 'baseline':10, 'amplitude':100},
        {'mu':180, 'sigma':10, 'baseline':0,  'amplitude':10},
        {'mu':180, 'sigma':4,  'baseline':0,  'amplitude':100},
        {'mu':180, 'sigma':20, 'baseline':0,  'amplitude':100},
        {'mu':30,  'sigma':10, 'baseline':0,  'amplitude':100},
        {'mu':330, 'sigma':10, 'baseline':0,  'amplitude':100},
        ]

    def gaussian_data(self, params):
        return measure.voltages_by_angle(
            lambda angle: fit_functions.gaussian(angle, **params))

    @unittest.skip('For visualization purposes only')
    def test_plot_with_gaussian_fit(self):
        for params in self.gaussian_params:
            with self.subTest(params):
                measure.plot_with_gaussian_fit(self.gaussian_data(params))

    def test_max_voltage(self):
        for params in self.gaussian_params:
            with self.subTest(params):
                max_voltage = measure.max_voltage(self.gaussian_data(params))
                self.assertAlmostEqual(max_voltage, params['amplitude'], 0)

    def test_max_voltage_angle(self):
        for params in self.gaussian_params:
            with self.subTest(params):
                max_voltage_angle = measure.max_voltage_angle(self.gaussian_data(params))
                self.assertGreaterEqual(max_voltage_angle, params['mu'] - 5)
                self.assertLess(max_voltage_angle, params['mu'] + 5)

    def test_expected_max_voltage_from_gaussian_fit(self):
        for params in self.gaussian_params:
            with self.subTest(params):
                expected_voltage = measure.expected_max_voltage_from_gaussian_fit(self.gaussian_data(params))
                self.assertAlmostEqual(expected_voltage, params['amplitude'], 0)

    def test_measurement_count(self):
        for params in self.gaussian_params:
            with self.subTest(params):
                measurement_count = measure.measurement_count(self.gaussian_data(params))
                self.assertGreaterEqual(measurement_count, 3)
                self.assertLessEqual(measurement_count, 18)

