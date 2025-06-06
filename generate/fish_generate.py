import random
from obj.fish import Fish

def generate_left_fishes(count, width, height, wall_x, gap_top, gap_bottom, line_width, radius=10, speed=0.08):
    """
    Generate the fish in left pool
    :param speed:
    :param count: the number of fish
    :param width: the width of left pool
    :param height: the height of left pool
    :param wall_x: the x coordinate of wall
    :param gap_top: the y coordinate of gap top
    :param gap_bottom: y coordinate of gap bottom
    :param line_width: wall thickness
    :param radius: fish size
    :return:
    """
    fishes = []
    left_pool = width // 2 - line_width

    while len(fishes) < count:
        x = random.uniform(0 + radius, left_pool - radius)
        y = random.uniform(0 + radius, height - radius)

        if Fish.is_valid_position(x, y, wall_x, gap_top, gap_bottom, line_width, radius):
            fishes.append(Fish(x, y, speed=speed))

    return fishes

def generate_right_fishes(count, width, height, wall_x, gap_top, gap_bottom, line_width, radius=10, speed=0.5):
    """
    Generate the fish in right pool
    :param speed:
    :param count: number of fish
    :param width: the width of right pool
    :param height: the height of right pool
    :param wall_x: the x coordinate of wall
    :param gap_top: the y coordinate of gap top
    :param gap_bottom: the y coordinate of gap bottom
    :param line_width: wall thickness
    :param radius: fish size
    :return:
    """
    fishes = []
    right_pool_left = width // 2 + line_width
    right_pool_right = width

    while len(fishes) < count:
        x = random.uniform(right_pool_left + radius, right_pool_right - radius)
        y = random.uniform(0 + radius, height - radius)

        if Fish.is_valid_position(x, y, wall_x, gap_top, gap_bottom, line_width, radius):
            fishes.append(Fish(x, y, speed=speed))

    return fishes
