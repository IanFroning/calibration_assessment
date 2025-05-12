import call_server
import measure

def get_measurement_data():
    if call_server.status_up() == False:
        print('Server reported as unavailable.')
    else:
        return measure.voltages_by_angle(call_server.get_measurement)

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

measurements = get_measurement_data()
if measurements:
    print_measurement_data(measurements)
    plot_measurement_data(measurements)
