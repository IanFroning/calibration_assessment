import requests
import measure

#TODO move to a server_wrapper module with actual error handling
def get_measurement(angle: float) -> float:
    result = requests.get('http://localhost:8000/measure', params={'angle': angle})
    return float(result.text)

def print_measurement_data(measurements):
    optimal_angle = measure.max_voltage_angle(measurements)
    optimal_voltage = measure.max_voltage(measurements)
    expected_voltage_from_fit = measure.expected_max_voltage_from_gaussian_fit(measurements)
    measurement_count = measure.measurement_count(measurements)
    print(f'Optimal response angle: {optimal_angle} degrees')
    print(f'Optimal response voltage: {optimal_voltage:.2f} V')
    print(f'Expected optimal voltage from fit: {expected_voltage_from_fit:.2f} V')
    print(f'Measurement count: {measurement_count}')

def plot_measurement_data(measurements):
    measure.plot_with_gaussian_fit(measurements)


measurements = measure.voltages_by_angle(get_measurement)
print_measurement_data(measurements)
plot_measurement_data(measurements)
