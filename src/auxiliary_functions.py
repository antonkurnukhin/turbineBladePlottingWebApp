import numpy as np
from numba import njit
from scipy.special import comb
from scipy.integrate import quad


@njit
def find_2d_intersection_point(
    x_coordinates_of_first_line: tuple, 
    y_coordinates_of_first_line: tuple, 
    x_coordinates_of_second_line: tuple, 
    y_coordinates_of_second_line: tuple):
    """Function to find the point of intersection of two two-dimensional lines

    https://www.cuemath.com/geometry/intersection-of-two-lines/
    """

    a_1 = y_coordinates_of_first_line[0] - y_coordinates_of_first_line[1]
    b_1 = x_coordinates_of_first_line[1] - x_coordinates_of_first_line[0]
    c_1 = x_coordinates_of_first_line[0] * y_coordinates_of_first_line[1] - \
        x_coordinates_of_first_line[1] * y_coordinates_of_first_line[0]

    a_2 = y_coordinates_of_second_line[0] - y_coordinates_of_second_line[1]
    b_2 = x_coordinates_of_second_line[1] - x_coordinates_of_second_line[0]
    c_2 = x_coordinates_of_second_line[0] * y_coordinates_of_second_line[1] - \
        x_coordinates_of_second_line[1] * y_coordinates_of_second_line[0]

    x_coordinate_of_interserction_point = -(c_1 * b_2 - c_2 * b_1) / (a_1 * b_2 - a_2 * b_1)
    y_coordinate_of_interserction_point = -(a_1 * c_2 - a_2 * c_1) / (a_1 * b_2 - a_2 * b_1)
    return (
        x_coordinate_of_interserction_point, 
        y_coordinate_of_interserction_point)


def calculate_bernstein_polynomial(i, n, t):
    """https://en.wikipedia.org/wiki/Bernstein_polynomial"""
    s = comb(n, i) * (t ** (n - i)) * (1 - t) ** i
    return s


def calculalate_bezier_curve_coordinates(
    base_points: tuple, 
    number_of_dots: int=200):

    number_of_dots = number_of_dots if \
        isinstance(number_of_dots, int) else \
        int(number_of_dots)

    number_of_points = len(base_points)
    x_coordinates = [p[0] for p in base_points]
    y_coordinates = [p[1] for p in base_points]

    t = np.linspace(0.0, 1.0, number_of_dots)

    polynomial_array = [
        calculate_bernstein_polynomial(i=i, n=number_of_points-1, t=t) for i in \
            range(0, number_of_points)]

    x_coordinates = np.array(x_coordinates)
    y_coordinates = np.array(y_coordinates)
    polynomial_array = np.array(polynomial_array)

    bezier_x_coordinates = np.dot(x_coordinates, polynomial_array)
    bezier_y_coordinates = np.dot(y_coordinates, polynomial_array)

    return (bezier_x_coordinates, bezier_y_coordinates)


def rotate_coordinates(data: dict):
    theta = -data['input_data']['beta_y']
    rotated_coordinates = (
        data['x_array'] * np.cos(theta) + data['y_array'] * -np.sin(theta),
        data['x_array'] * np.sin(theta) + data['y_array'] * np.cos(theta)
    )

    return rotated_coordinates


def calculate_blade_area(blade: dict):
    rotated_x, rotated_y = rotate_coordinates(blade_data=blade)

    x_max = np.argmax(rotated_x)
    x_min = np.argmin(rotated_x)

    front_x = rotated_x[x_max:x_min+1]
    front_y = rotated_y[x_max:x_min+1]
    back_x = np.delete(rotated_x, slice(x_max+1, x_min))
    back_y = np.delete(rotated_y, slice(x_max+1, x_min))

    sorted_back = sorted(zip(back_x, back_y), key=lambda x: x[0])

    back_x = [c[0] for c in sorted_back]
    back_y = [c[1] for c in sorted_back]

    area = quad(
        lambda x: abs(np.interp(x, back_x, back_y) - np.interp(x, front_x, front_y)),
        rotated_x[x_min],
        rotated_x[x_max]
    )[0]
    return area
    
