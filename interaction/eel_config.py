# interaction/eel_config.py
import random

# 默认属性配置（初始状态）
DEFAULT_EEL_PROPERTIES = {
    'left': {
        'slow_factor': 2,
        'reward_growth_factor': 0.15,
        'max_reward_probability': 0.7  # 初始左鳗鱼概率
    },
    'right': {
        'slow_factor': 0.9,
        'reward_growth_factor': 0.25,
        'max_reward_probability': 0.9  # 初始右鳗鱼概率
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
        return DEFAULT_EEL_PROPERTIES[side].copy()

    if _swapped:    # 次轮回合，发生交换的情况
        if side == 'left':
            return _last_choice_prop["right"].copy()
        elif side == 'right':
            return _last_choice_prop["left"].copy()
    else:   # 次轮回合，未发生交换的情况
        return _last_choice_prop[side].copy()


def maybe_swap_eel_properties(mu=0.5, sigma=0.1, swap_threshold=0.5):
    """依据高斯分布决定是否对调属性（严格保持max_prob规则）"""
    global _swapped, _last_choice_prop

    # 始终记录当前右侧max_prob（用于下一轮保持）
    current_right_prop = DEFAULT_EEL_PROPERTIES
    _last_choice_prop = current_right_prop

    # 决定是否交换
    score = random.gauss(mu, sigma)
    if score > swap_threshold:
        _swapped = not _swapped
        _last_choice_prop['left'], _last_choice_prop['right'] = DEFAULT_EEL_PROPERTIES['right'], DEFAULT_EEL_PROPERTIES['left']

    return _swapped


def is_swapped():
    """当前是否处于对调状态"""
    return _swapped