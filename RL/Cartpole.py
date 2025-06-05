import gymnasium as gym
from gymnasium import pprint_registry

env = gym.make('CartPole-v1', render_mode='human')  # 允许可视化
# pprint_registry()
obs, info = env.reset()  # 初始化环境

for _ in range(10000):  # 运行 1000 步
    action = env.action_space.sample()  # 选择随机动作（0 或 1）
    obs, reward, terminated, truncated, info = env.step(action)  # 执行动作
    if terminated or truncated:
        obs, info = env.reset()  # 重新开始

env.close()  # 关闭环境
