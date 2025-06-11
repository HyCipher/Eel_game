import random

from interaction.eel_config import get_eel_properties
from obj.eel import Eel


def generate_left_eels(count, width, height, wall_x, line_width, radius):
    eels = []

    # 左边鱼池范围
    left_pool_x_min = 0
    left_pool_x_max = wall_x - line_width // 2 - radius

    for _ in range(count):
        # left_eel生成位置
        x = left_pool_x_max // 2
        y = height // 2
        eels.append(Eel(x, y, get_eel_properties('left')['slow_factor']))

    return eels


def generate_right_eels(count, width, height, wall_x, line_width, radius):
    eels = []

    # 右边鱼池范围
    right_pool_x_min = wall_x + line_width // 2 + radius
    right_pool_x_max = width

    for _ in range(count):
        # right_eel生成位置
        x = (right_pool_x_max - right_pool_x_min) // 2 + right_pool_x_min
        y = height // 2
        eels.append(Eel(x, y, get_eel_properties('right')['slow_factor']))

    return eels