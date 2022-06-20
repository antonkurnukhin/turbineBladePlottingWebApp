from numba import njit


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

    
