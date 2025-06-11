import numpy as np
import random
from collections import defaultdict


class SarsaAgent:
    def __init__(self, state_size, action_size,
                 learning_rate=0.1, gamma=0.99,
                 epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        """
        SARSA 算法实现

        参数:
            state_size: 状态维度
            action_size: 动作数量
            learning_rate: 学习率 (α)
            gamma: 折扣因子
            epsilon: 探索率
            epsilon_decay: 探索率衰减
            epsilon_min: 最小探索率
        """
        self.q_table = defaultdict(lambda: np.zeros(action_size))
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.action_size = action_size

    def get_action(self, state, training=True):
        """ε-贪婪策略选择动作"""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state, next_action, done):
        """SARSA 更新规则"""
        current_q = self.q_table[state][action]
        next_q = self.q_table[next_state][next_action] if not done else 0

        # SARSA 更新公式
        self.q_table[state][action] += self.lr * (
                reward + self.gamma * next_q - current_q
        )

        # 衰减探索率
        if done:
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


class FishGameEnv:
    # ... (保持之前的实现不变)

    def _get_observation(self):
        """将状态转换为可哈希的元组"""
        # 获取所有观测值（与之前相同）
        obs_values = [
            self.player.x / self.canvas.width,
            self.player.y / self.canvas.height,
            # ... 其他归一化值 ...
        ]

        # 将浮点数离散化以便Q表处理
        discrete_state = tuple(int(x * 10) for x in obs_values)  # 将状态空间离散化为10个区间
        return discrete_state


def train_sarsa():
    # 初始化环境
    canvas = Canvas()
    env = FishGameEnv(canvas)

    # 初始化SARSA智能体
    state_size = len(env.reset())
    agent = SarsaAgent(state_size=state_size, action_size=env.action_space)

    try:
        for episode in range(1000):  # 训练1000轮
            state = env.reset()
            action = agent.get_action(state)

            total_reward = 0
            done = False

            while not done:
                # 执行动作
                next_state, reward, done, info = env.step(action)

                # 选择下一个动作
                next_action = agent.get_action(next_state)

                # 更新Q表
                agent.update(state, action, reward, next_state, next_action, done)

                # 更新状态和动作
                state, action = next_state, next_action
                total_reward += reward

                # 可选：渲染画面（会降低训练速度）
                # env.render()

            print(f"Episode {episode + 1}, Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")

            # 每100轮保存一次Q表
            if episode % 100 == 0:
                save_q_table(agent.q_table, f"sarsa_qtable_ep{episode}.pkl")

    finally:
        env.close()


def save_q_table(q_table, filename):
    """保存Q表到文件"""
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(dict(q_table), f)