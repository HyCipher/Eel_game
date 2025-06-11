# interaction.py
import math


def check_collision(x1, y1, r1, x2, y2, r2):
    """判断两个圆形是否碰撞"""
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance < (r1 + r2)


def check_eel_activation(player, eels, fishes, wall_x):
    """
    玩家碰到鳗鱼时，捕获该鳗鱼电场内的所有鱼，并返回 eel 所在的边。
    参数：
        player: Player 对象
        eels: list of Eel 对象
        fishes: list of Fish 对象
        wall_x: 墙体的 x 坐标，用于判断鱼是否在同一边

    返回：
        (captured_fishes, eel_side) 或 None
    """
    for eel in eels:
        if check_collision(player.x, player.y, player.radius, eel.x, eel.y, eel.radius):
            # 判断 eel 是左侧还是右侧的
            eel_side = 'left' if eel.x < wall_x else 'right'

            # 收集该 eel 电场范围内的鱼
            captured_fishes = [
                fish for fish in fishes if eel.affects(fish, wall_x)
            ]
            return captured_fishes, eel_side

    return None
