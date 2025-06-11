# interaction/eel_config.py
import random

# 默认属性配置（初始状态）
DEFAULT_EEL_PROPERTIES = {
    'left': {
        'slow_factor': 0.2,
        'reward_growth_factor': 0.25,
        'max_reward_probability': 0.75
    },
    'right': {
        'slow_factor': 1,
        'reward_growth_factor': 0.1,
        'max_reward_probability': 0.3
    }
}

# 状态跟踪
_swapped = False
_last_choice_prop = None

def get_eel_properties(side):
    """
    获取接触一侧的eel属性
    """
    if _last_choice_prop is None:   # 首轮回合
        return DEFAULT_EEL_PROPERTIES[side]
    else:
        if _swapped:    # 次轮回合，发生交换的情况
            if side == 'left':
                return DEFAULT_EEL_PROPERTIES['right']
            elif side == 'right':
                return DEFAULT_EEL_PROPERTIES['left']
        else:   # 次轮回合，未发生交换的情况
            return DEFAULT_EEL_PROPERTIES[side]


# def maybe_swap_eel_properties(mu=0.35, sigma=0.1, swap_threshold=0.5):
def maybe_swap_eel_properties(swap_prob=0.3):
    """依据高斯分布决定是否对调属性（严格保持max_prob规则）"""
    global _swapped
    swapped_temp = _swapped

    # 决定是否交换
    # score = random.gauss(mu, sigma)

    # if score > swap_threshold:
    if random.random() < swap_prob:
        swapped_temp = not swapped_temp
        DEFAULT_EEL_PROPERTIES['left'], DEFAULT_EEL_PROPERTIES['right'] = DEFAULT_EEL_PROPERTIES['right'], DEFAULT_EEL_PROPERTIES['left']

    # print(swapped_temp, DEFAULT_EEL_PROPERTIES)
    return swapped_temp

def swapped_reset():
    """swapped to false"""
    _swapped = False