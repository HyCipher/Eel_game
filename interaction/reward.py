# interaction/reward.py

import random
from interaction.eel_config import get_eel_properties


def evaluate_reward(captured_fish_count, eel_side):
    """
    根据 eel 所在边（left/right）和捕获的鱼数量，评估是否获得奖励。

    参数：
        captured_fish_count: 捕获的鱼的数量
        eel_side: 'left' 或 'right'

    返回：
    +    got_reward (bool): 是否获得奖励
    """
    # 获取所在侧的eel属性
    config = get_eel_properties(eel_side)

    growth_factor = config['reward_growth_factor']
    max_probability = config['max_reward_probability']

    probability = min(captured_fish_count * growth_factor, max_probability)

    print(f"competency = {config['slow_factor']}")
    print(f"reliability = {probability}")

    # 判断是否获得reward
    got_reward = random.random() < probability

    return got_reward
