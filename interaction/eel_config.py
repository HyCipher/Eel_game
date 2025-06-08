# interaction/eel_config.py
import random

# 模块级变量记录是否对调了
_swapped = False

def maybe_swap_eel_properties(mu=0.5, sigma=0.1, swap_threshold=0.5):
    """
    依据高斯分布决定是否对调左右 eel 的属性。
    """
    global _swapped
    score = random.gauss(mu, sigma)
    if score > swap_threshold:
        _swapped = not _swapped  # 只有在触发时才反转
    return _swapped

def get_eel_properties(eel_side):
    """
    返回特定 eel 所在侧的行为配置：
    - 减速因子（越大表示电场越强，鱼越慢）
    - reward_growth_factor：捕到鱼数量转 reward 概率的增长系数
    - max_reward_probability：奖励概率上限
    """
    if (_swapped and eel_side == 'left') or (not _swapped and eel_side == 'right'):
        # 当前这个 eel 是“快强奖励高”的那一边
        print("对调状态（是否左右互换）:", _swapped)
        return {
            'slow_factor': 0.7,
            'reward_growth_factor': 0.25,
            'max_reward_probability': 0.9
        }
    else:
        # 当前这个 eel 是“慢弱奖励低”的那一边
        return {
            'slow_factor': 0.2,
            'reward_growth_factor': 0.15,
            'max_reward_probability': 0.7
        }

def is_swapped():
    """提供当前是否对调的状态供外部查看（调试用）"""
    return _swapped