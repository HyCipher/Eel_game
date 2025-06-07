# interaction/reward.py

import random


def evaluate_reward(captured_fish_count, eel_side='left'):
    """
    根据 eel 所在边（left/right）和捕获的鱼数量，评估是否获得奖励。

    参数：
        captured_fish_count: 捕获的鱼的数量
        eel_side: 'left' 或 'right'

    返回：
        got_reward (bool): 是否获得奖励
    """
    if eel_side == 'left':
        max_probability = 0.7
    elif eel_side == 'right':
        max_probability = 0.9
    else:
        max_probability = 0.1  # fallback

    probability = min(captured_fish_count * 0.2, max_probability)
    got_reward = random.random() < probability
    return got_reward
