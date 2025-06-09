# interaction/eel_config.py
import random

# 默认属性配置（初始状态）
DEFAULT_EEL_PROPERTIES = {
    'left': {
        'slow_factor': 0.2,
        'reward_growth_factor': 0.15,
        'max_reward_probability': 0.7  # 初始左鳗鱼概率
    },
    'right': {
        'slow_factor': 0.7,
        'reward_growth_factor': 0.25,
        'max_reward_probability': 0.9  # 初始右鳗鱼概率
    }
}

# 状态跟踪
_swapped = False
_last_right_max_prob = None  # 专门记录右侧上一轮的max_prob


def get_eel_properties(side):
    """获取指定侧的鳗鱼属性（自动处理max_prob的保持）"""
    props = DEFAULT_EEL_PROPERTIES[side].copy()

    # 如果未交换且存在上一轮的记录，则强制保持右侧max_prob
    if not _swapped and _last_right_max_prob is not None and side == 'right':
        props['max_reward_probability'] = _last_right_max_prob

    return props


def maybe_swap_eel_properties(mu=0.5, sigma=0.1, swap_threshold=0.5):
    """依据高斯分布决定是否对调属性（严格保持max_prob规则）"""
    global _swapped, _last_right_max_prob

    # 始终记录当前右侧max_prob（用于下一轮保持）
    current_right_prob = DEFAULT_EEL_PROPERTIES['right']['max_reward_probability']
    _last_right_max_prob = current_right_prob

    # 决定是否交换
    score = random.gauss(mu, sigma)
    if score > swap_threshold:
        _swapped = not _swapped
        # 交换时只交换max_reward_probability（其他属性不变）
        DEFAULT_EEL_PROPERTIES['left']['max_reward_probability'], DEFAULT_EEL_PROPERTIES['right'][
            'max_reward_probability'] = \
            DEFAULT_EEL_PROPERTIES['right']['max_reward_probability'], DEFAULT_EEL_PROPERTIES['left'][
                'max_reward_probability']

    return _swapped


def is_swapped():
    """当前是否处于对调状态"""
    return _swapped