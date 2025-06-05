# interaction.py
import math


def check_collision(x1, y1, r1, x2, y2, r2):
    """判断两个圆形是否碰撞"""
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance < (r1 + r2)


def handle_player_fish_interactions(player, fish_lists):
    """
    玩家与鱼的交互处理：检查是否抓到鱼，抓到则从鱼列表中移除。

    参数：
        player: Player 对象，需包含 x, y, radius 属性
        fish_lists: list of list，例如 [left_fishes, right_fishes]
    """
    for fish_list in fish_lists:
        caught_fish = []
        for fish in fish_list:
            if check_collision(player.x, player.y, player.radius, fish.x, fish.y, fish.radius):
                caught_fish.append(fish)
        for fish in caught_fish:
            fish_list.remove(fish)
