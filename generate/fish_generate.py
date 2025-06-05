import random
from obj.fish import Fish

def generate_left_fishes(count, width, height, wall_x, gap_top, gap_bottom, line_width, radius=10):
    """
    Generate the fish in left pool
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
        x = random.uniform(0, left_pool)
        y = random.uniform(0, height)

        if Fish.is_valid_position(x, y, wall_x, gap_top, gap_bottom, line_width, radius):
            fishes.append(Fish(x, y))

    return fishes

def generate_right_fishes(count, width, height, wall_x, gap_top, gap_bottom, line_width, radius=10):
    """
    Generate the fish in right pool
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
        x = random.uniform(right_pool_left, right_pool_right)
        y = random.uniform(0, height)

        if Fish.is_valid_position(x, y, wall_x, gap_top, gap_bottom, line_width, radius):
            fishes.append(Fish(x, y))

    return fishes
