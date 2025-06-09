# interaction.py
import math
from utils.logger import log_game_round
from interaction.reward import evaluate_reward


def handle_game_over(captured_fishes, eel_side, round_number, is_swapped):
    fish_count = len(captured_fishes)
    print(f"Round {round_number} Over! You captured {fish_count} fish from the {eel_side} eel")

    got_reward, config = evaluate_reward(fish_count, eel_side)

    if got_reward:
        print("🎉 You received a reward!")
    else:
        print("No reward this time. Try again!")

    # ✅ 写入日志
    # log_game_round(round_number, eel_side, fish_count, got_reward, config,  swapped=is_swapped)


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
