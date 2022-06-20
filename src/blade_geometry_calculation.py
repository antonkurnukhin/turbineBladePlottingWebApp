from pprint import pprint
import numpy as np
from auxiliary_functions import calculalate_bezier_curve_coordinates, \
    find_2d_intersection_point

PI_2 = np.pi / 2.


def create_blade_section(
        blade_chord: float,
        blade_inlet_angle: float,
        blade_outlet_angle: float,
        blade_installation_angle: float,
        blade_inlet_opening_angle: float,
        blade_outlet_opening_angle: float,
        leading_edge_radius: float,
        trailing_edge_radius: float,
        inlet_flow_speed: float,
        outlet_flow_speed: float,
        number_of_dots_for_bezier_curve: int=200):

    number_of_dots_for_bezier_curve = number_of_dots_for_bezier_curve if \
        isinstance(number_of_dots_for_bezier_curve, int) else \
        int(number_of_dots_for_bezier_curve)
    number_of_dots_for_edge_arc_bezier_curve = int(number_of_dots_for_bezier_curve/5)
    # precalculation
    inlet_opening_angle_minus_2 = blade_inlet_angle - blade_inlet_opening_angle / 2.
    inlet_opening_angle_plus_2 = blade_inlet_angle + blade_inlet_opening_angle / 2.
    outlet_opening_angle_minus_2 = blade_outlet_angle - blade_outlet_opening_angle / 2.
    outlet_opening_angle_plus_2 = blade_outlet_angle + blade_outlet_opening_angle / 2.

    # main points
    x_1: float = 0.
    y_1: float = 0.
    x_2: float = x_1 + blade_chord * np.tan(blade_installation_angle-PI_2)
    y_2: float = y_1 - blade_chord

    # Это точка l
    x_1_back: float = x_1 + leading_edge_radius * np.cos(PI_2 + inlet_opening_angle_minus_2)
    y_1_back: float = y_1 + leading_edge_radius * np.sin(PI_2 + inlet_opening_angle_minus_2)
    x_1w_back: float = x_1_back + inlet_flow_speed * np.cos(inlet_opening_angle_minus_2)
    y_1w_back: float = y_1_back + inlet_flow_speed * np.sin(inlet_opening_angle_minus_2)

    # Это точка g
    x_1_front: float = x_1 + leading_edge_radius * np.cos(inlet_opening_angle_plus_2 - PI_2)
    y_1_front: float = y_1 + leading_edge_radius * np.sin(inlet_opening_angle_plus_2 - PI_2)
    x_1w_front: float = x_1_front + inlet_flow_speed * np.cos(inlet_opening_angle_plus_2)
    y_1w_front: float = y_1_front + inlet_flow_speed * np.sin(inlet_opening_angle_plus_2)

    x_2_back: float = x_2 + trailing_edge_radius * np.cos(outlet_opening_angle_plus_2 + PI_2)
    y_2_back: float = y_2 + trailing_edge_radius * np.sin(outlet_opening_angle_plus_2 + PI_2)
    x_2w_back: float = x_2_back - outlet_flow_speed * np.cos(outlet_opening_angle_plus_2)
    y_2w_back: float = y_2_back - outlet_flow_speed * np.sin(outlet_opening_angle_plus_2)

    x_2_front: float = x_2 + trailing_edge_radius * np.cos(outlet_opening_angle_minus_2 - PI_2)
    y_2_front: float = y_2 + trailing_edge_radius * np.sin(outlet_opening_angle_minus_2 - PI_2)
    x_2w_front: float = x_2_front - outlet_flow_speed * np.cos(outlet_opening_angle_minus_2)
    y_2w_front: float = y_2_front - outlet_flow_speed * np.sin(outlet_opening_angle_minus_2)

    back_intersection_point: tuple = find_2d_intersection_point(
        x_coordinates_of_first_line=(x_1_back, x_1w_back), 
        y_coordinates_of_first_line=(y_1_back, y_1w_back),
        x_coordinates_of_second_line=(x_2_back, x_2w_back), 
        y_coordinates_of_second_line=(y_2_back, y_2w_back)
    )

    front_intersection_point: tuple = find_2d_intersection_point(
        x_coordinates_of_first_line=(x_1_front, x_1w_front), 
        y_coordinates_of_first_line=(y_1_front, y_1w_front),
        x_coordinates_of_second_line=(x_2_front, x_2w_front), 
        y_coordinates_of_second_line=(y_2_front, y_2w_front)
    )

    points_for_back_bezier_line: tuple = (
        (x_1_back, y_1_back, 0.),
        (back_intersection_point[0], back_intersection_point[1], 0.),
        (x_2_back, y_2_back, 0.),
    )
    points_for_front_bezier_line: tuple = (
        (x_1_front, y_1_front, 0.),
        (front_intersection_point[0], front_intersection_point[1], 0.),
        (x_2_front, y_2_front, 0.),
    )

    back: tuple = calculalate_bezier_curve_coordinates(
        base_points=points_for_back_bezier_line, 
        number_of_dots=number_of_dots_for_bezier_curve)
    front: tuple = calculalate_bezier_curve_coordinates(
        base_points=points_for_front_bezier_line, 
        number_of_dots=number_of_dots_for_bezier_curve)

    leading_edge_start_angle: float = PI_2 + (blade_inlet_angle - blade_inlet_opening_angle / 2.)
    leading_edge_end_angle: float = (blade_inlet_angle + blade_inlet_opening_angle / 2.) - PI_2
    leading_edge_angles = np.linspace(
        leading_edge_start_angle, 
        leading_edge_end_angle, 
        number_of_dots_for_edge_arc_bezier_curve)
    leading_edge_x = x_1 + leading_edge_radius * np.cos(leading_edge_angles)
    leading_edge_y = y_1 + leading_edge_radius * np.sin(leading_edge_angles)

    trainling_edge_start_angle: float = (blade_outlet_angle - blade_outlet_opening_angle / 2.) + PI_2 - np.pi
    trainling_edge_end_angle: float = (blade_outlet_angle + blade_outlet_opening_angle / 2.) - PI_2 - np.pi
    trainling_edge_angles = np.linspace(
        trainling_edge_start_angle, 
        trainling_edge_end_angle, 
        number_of_dots_for_edge_arc_bezier_curve)
    trainling_edge_x = x_2 + trailing_edge_radius * np.cos(trainling_edge_angles)
    trainling_edge_y = y_2 + trailing_edge_radius * np.sin(trainling_edge_angles)

    x, y = back
    x, y = np.append(x, leading_edge_x), np.append(y, leading_edge_y)
    x, y = np.append(x, np.flip(front[0])), np.append(y, np.flip(front[1]))
    x, y = np.append(x, trainling_edge_x), np.append(y, trainling_edge_y)

    ones = np.ones(len(x))
    center_of_mass: tuple = (
        np.sum(x * ones) / np.sum(ones), 
        np.sum(y * ones) / np.sum(ones), 
        0.)

    x_array = x - center_of_mass[0]
    y_array = y - center_of_mass[1]

    return {
        'input_data': {
            'blade_chord': blade_chord,
            'blade_inlet_angle': blade_inlet_angle,
            'blade_outlet_angle': blade_outlet_angle,
            'blade_installation_angle': blade_installation_angle,
            'blade_inlet_opening_angle': blade_inlet_opening_angle,
            'blade_outlet_opening_angle': blade_outlet_opening_angle,
            'leading_edge_radius': leading_edge_radius,
            'trailing_edge_radius': trailing_edge_radius,
            'inlet_flow_speed': inlet_flow_speed,
            'outlet_flow_speed': outlet_flow_speed,
        },
        'x_array': x_array,
        'y_array': y_array,
    }


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    blade_type = 0  # 0 --- turbine; 1 --- compressor

    if blade_type == 0:
        turbine_blade_chord = 28.3
        turbine_blade_inlet_angle = np.radians(30.)
        turbine_blade_outlet_angle = np.pi-np.radians(30.)
        turbine_blade_installation_angle = (
            turbine_blade_inlet_angle+turbine_blade_outlet_angle)/2.
        turbine_blade_inlet_opening_angle = np.radians(10.)
        turbine_blade_outlet_opening_angle = np.radians(8.)
        turbine_leading_edge_radius = turbine_blade_chord*0.025
        turbine_trailing_edge_radius = turbine_blade_chord*0.01
        turbine_inlet_flow_speed = 100.
        turbine_outlet_flow_speed = 100.

        blade_data = create_blade_section(
            blade_chord=turbine_blade_chord, 
            blade_inlet_angle=turbine_blade_inlet_angle, 
            blade_outlet_angle=turbine_blade_outlet_angle, 
            blade_installation_angle=turbine_blade_installation_angle, 
            blade_inlet_opening_angle=turbine_blade_inlet_opening_angle,
            blade_outlet_opening_angle=turbine_blade_outlet_opening_angle, 
            leading_edge_radius=turbine_leading_edge_radius, 
            trailing_edge_radius=turbine_trailing_edge_radius,
            inlet_flow_speed=turbine_inlet_flow_speed, 
            outlet_flow_speed=turbine_outlet_flow_speed)
    else:
        compressor_blade_chord = 30.
        compressor_blade_inlet_angle = np.radians(30.)
        compressor_blade_outlet_angle = np.radians(50.)
        compressor_blade_installation_angle = (
            compressor_blade_inlet_angle + compressor_blade_outlet_angle) / 2.
        compressor_blade_inlet_opening_angle = np.radians(6.)
        compressor_blade_outlet_opening_angle = np.radians(4.)
        compressor_leading_edge_radius = 0.1
        compressor_trailing_edge_radius = 0.1
        compressor_inlet_flow_speed = 100.
        compressor_outlet_flow_speed = 100.

        blade_data = create_blade_section(
            blade_chord=compressor_blade_chord, 
            blade_inlet_angle=compressor_blade_inlet_angle,
            blade_outlet_angle=compressor_blade_outlet_angle, 
            blade_installation_angle=compressor_blade_installation_angle, 
            blade_inlet_opening_angle=compressor_blade_inlet_opening_angle,
            blade_outlet_opening_angle=compressor_blade_outlet_opening_angle, 
            leading_edge_radius=compressor_leading_edge_radius, 
            trailing_edge_radius=compressor_trailing_edge_radius,
            inlet_flow_speed=compressor_inlet_flow_speed, 
            outlet_flow_speed=compressor_outlet_flow_speed)

    pprint(blade_data)
    plt.plot(blade_data['x_array'], blade_data['y_array'])
    plt.plot([0.], [0.], 'ro')
    plt.axis('equal')
    plt.show()