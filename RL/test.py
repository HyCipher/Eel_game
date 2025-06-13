from rl_env import EelGameEnv
from qlearning import QLearningAgent

# 初始化环境
env = EelGameEnv()  # 去掉render_mode可加速训练

# 设置学习参数
learning_params = {
    'epsilon': 1.0,      # 初始探索率
    'min_epsilon': 0.01, # 最小探索率
    'epsilon_decay': 0.995, # 探索率衰减
    'alpha': 0.7,        # 初始学习率
    'alpha_decay': 0.995, # 学习率衰减
    'gamma': 0.95        # 折扣因子
}

# 创建智能体
agent = QLearningAgent(env, learning_params)

# 开始训练
rewards_history = agent.train(episodes=500)

# 保存Q-table (可选)
import pickle
with open('q_table.pkl', 'wb') as f:
    pickle.dump(dict(agent.q_table), f)