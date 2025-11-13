import math

from panda3d.core import Point2

_PRECISION = 2


def rotate_point(
    x: float,
    y: float,
    cx: float,
    cy: float,
    angle_degrees: float,
) -> Point2:
    """
    Rotate a point around a center.

    Args:
        x (float): x value of the point you want to rotate
        y (float): y value of the point you want to rotate
        cx (float): x value of the center point you want to rotate around
        cy (float): y value of the center point you want to rotate around
        angle_degrees (float): Angle, in degrees, to rotate
    """
    temp_x = x - cx
    temp_y = y - cy

    # now apply rotation
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    rotated_x = temp_x * cos_angle + temp_y * sin_angle
    rotated_y = -temp_x * sin_angle + temp_y * cos_angle

    # translate back
    x = round(rotated_x + cx, _PRECISION)
    y = round(rotated_y + cy, _PRECISION)

    return Point2(x, y)
