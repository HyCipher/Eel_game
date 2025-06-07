# interaction.py
import math
import pygame
from interaction.reward import evaluate_reward


def handle_game_over(captured_fishes, eel_side):
    fish_count = len(captured_fishes)
    print(f"Game Over! You captured {fish_count} fish from the {eel_side} eel")

    if evaluate_reward(fish_count):
        print("🎉 You received a reward!")
    else:
        print("No reward this time. Try again!")

    pygame.quit()
    exit()

def check_collision(x1, y1, r1, x2, y2, r2):
    """判断两个圆形是否碰撞"""
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance < (r1 + r2)

# def check_eel_activation(player, eels, fishes, wall_x):
#     """
#     玩家碰到鳗鱼时，捕获该鳗鱼电场内的所有鱼。
#     When the player encounters an eel, capture all fish within the eel's electric field.
#     参数：
#         player: Player 对象
#         eels: list of Eel 对象
#         fishes: list of Fish 对象
#         wall_x: 墙体的 x 坐标，用于判断鱼是否在同一边
#
#     返回：
#         被捕获的鱼列表
#     """
#     captured_fishes = []
#
#     for eel in eels:
#         if check_collision(player.x, player.y, player.radius, eel.x, eel.y, eel.radius):
#             # 玩家碰到了 eel，则收集该 eel 电场范围内的鱼
#             for fish in fishes:
#                 if eel.affects(fish, wall_x):
#                     captured_fishes.append(fish)
#
#     return captured_fishes

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
