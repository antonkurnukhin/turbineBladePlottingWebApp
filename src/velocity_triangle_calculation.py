import numpy as np
from numba import njit


# @njit()
def calculate_velocity_triangle(
    inlet_absolute_velocity: float,
    outlet_absolute_velocity: float,
    inlet_relative_velocity: float,
    outlet_relative_velocity: float,
    inlet_absolute_angle: float,
    outlet_absolute_angle: float,
    inlet_relative_angle: float,
    outlet_relative_angle: float,
    scale: float = 1,
    vector_opening_angle: float=10):
    message = ''

    # radians
    inlet_absolute_angle = np.radians(inlet_absolute_angle)
    outlet_absolute_angle = np.radians(outlet_absolute_angle)
    inlet_relative_angle = np.radians(inlet_relative_angle)
    outlet_relative_angle = np.radians(outlet_relative_angle)
    vector_opening_angle = np.radians(vector_opening_angle)

    if outlet_absolute_angle <= 0.:
        outlet_absolute_angle = np.pi + outlet_absolute_angle
    if outlet_relative_angle <= 0.:
        outlet_relative_angle = np.pi + outlet_relative_angle

    inlet_absolute_x = -inlet_absolute_velocity * np.cos(inlet_absolute_angle)
    inlet_absolute_y = -inlet_absolute_velocity * np.sin(inlet_absolute_angle)
    inlet_relative_x =  -inlet_relative_velocity * np.cos(inlet_relative_angle)
    inlet_relative_y=  -inlet_relative_velocity * np.sin(inlet_relative_angle)

    outlet_absolute_x = -outlet_absolute_velocity * np.cos(outlet_absolute_angle)
    outlet_absolute_y = -outlet_absolute_velocity * np.sin(outlet_absolute_angle)
    outlet_relative_x = outlet_relative_velocity * np.cos(-outlet_relative_angle)
    outlet_relative_y = outlet_relative_velocity * np.sin(-outlet_relative_angle)

    inlet_absolute_coordinates = ((0., inlet_absolute_x), (0., inlet_absolute_y))
    inlet_relative_coordinates = ((0., inlet_relative_x), (0., inlet_relative_y))

    outlet_absolute_coordinates = ((0., outlet_absolute_x), (0., outlet_absolute_y))
    outlet_relative_coordinates = ((0., outlet_relative_x), (0., outlet_relative_y))
    
    # TODO vector arrows

    circumferential_velocity_0 = np.sqrt(
        (inlet_absolute_x - inlet_relative_x) ** 2 + 
        (inlet_absolute_y - inlet_relative_y) ** 2)
    circumferential_velocity_1 = np.sqrt(
        (outlet_absolute_x - outlet_relative_x) ** 2 + 
        (outlet_absolute_y - outlet_relative_y) ** 2)

    if circumferential_velocity_0!=circumferential_velocity_1:
        message = 'Окружные скорости на входе в рабочий венец и на выходе из него не равны. Возможно, допущена ошибка в расчёта газодинамики.'
        message_en = 'Peripheral speeds at the entrance to the working crown and at the exit from it are not available. Perhaps an error was made in the calculation of gas dynamics.'

    return {
        'inlet_absolute_coordinates': inlet_absolute_coordinates,
        'inlet_relative_coordinates': inlet_relative_coordinates,
        'outlet_absolute_coordinates': outlet_absolute_coordinates,
        'outlet_relative_coordinates': outlet_relative_coordinates,
        'message': message,
    }


if __name__ =='__main__':
    from pprint import pprint
    import matplotlib.pyplot as plt

    c_1 = 649.6
    c_2 = 265.0
    w_1 = 399
    w_2 = 438.3
    absolute_motion_angle_1 = 23.97
    absolute_motion_angle_2 = 103.03
    relative_motion_angle_1 = 41.41
    relative_motion_angle_2 = 36.09

    data = calculate_velocity_triangle(
        inlet_absolute_velocity=c_1,
        outlet_absolute_velocity=c_2,
        inlet_relative_velocity=w_1,
        outlet_relative_velocity=w_2,
        inlet_absolute_angle=absolute_motion_angle_1,
        outlet_absolute_angle=absolute_motion_angle_2,
        inlet_relative_angle=relative_motion_angle_1,
        outlet_relative_angle=relative_motion_angle_2)

    pprint(data)

    plt.plot(data['inlet_absolute_coordinates'][0], data['inlet_absolute_coordinates'][1], label='c_1')
    plt.plot(data['inlet_relative_coordinates'][0], data['inlet_relative_coordinates'][1], label='w_1')
    plt.plot(data['outlet_absolute_coordinates'][0], data['outlet_absolute_coordinates'][1], label='c_2')
    plt.plot(data['outlet_relative_coordinates'][0], data['outlet_relative_coordinates'][1], label='w_2')
    plt.legend()
    plt.show()
