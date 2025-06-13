import numpy as np
import random
from collections import defaultdict


class QLearningAgent:
    def __init__(self, env, learning_params):
        """
        初始化Q-learning智能体

        参数:
            env: 游戏环境
            learning_params: 包含学习参数的字典 {
                'epsilon': 初始探索率,
                'min_epsilon': 最小探索率,
                'epsilon_decay': 探索率衰减率,
                'alpha': 初始学习率,
                'alpha_decay': 学习率衰减率,
                'gamma': 折扣因子
            }
        """
        self.env = env
        self.q_table = defaultdict(lambda: np.zeros(env.action_space.n))

        # 学习参数
        self.epsilon = learning_params['epsilon']
        self.min_epsilon = learning_params['min_epsilon']
        self.epsilon_decay = learning_params['epsilon_decay']
        self.alpha = learning_params['alpha']
        self.alpha_decay = learning_params['alpha_decay']
        self.gamma = learning_params['gamma']

        # 状态离散化参数
        self.bins = {
            'player_x': 10,
            'player_y': 10,
            'wall_gap': 5
        }

    def _discretize_state(self, state):
        """
        将连续状态空间离散化为Q-table的键
        """
        # 示例离散化方法 - 您可以根据需要调整
        player_x = np.digitize(state['player'][0], np.linspace(0, self.env.canvas.width, self.bins['player_x']))
        player_y = np.digitize(state['player'][1], np.linspace(0, self.env.canvas.height, self.bins['player_y']))

        # 使用墙壁间隙信息
        wall_gap = np.digitize(state['wall'][1] - state['wall'][0],
                               np.linspace(0, self.env.canvas.height, self.bins['wall_gap']))

        # 返回离散化后的状态键
        return (player_x, player_y, wall_gap)

    def get_action(self, state):
        """
        使用ε-贪婪策略选择动作
        """
        discretized_state = self._discretize_state(state)

        if random.random() < self.epsilon:
            # 探索: 随机选择动作
            return self.env.action_space.sample()
        else:
            # 利用: 选择Q值最高的动作
            return np.argmax(self.q_table[discretized_state])

    def update(self, state, action, reward, next_state, done):
        """
        更新Q-table
        """
        discretized_state = self._discretize_state(state)
        discretized_next_state = self._discretize_state(next_state)

        # Q-learning更新公式
        current_q = self.q_table[discretized_state][action]
        max_next_q = np.max(self.q_table[discretized_next_state])

        # 计算目标Q值
        target_q = reward + (1 - done) * self.gamma * max_next_q

        # 更新Q值
        self.q_table[discretized_state][action] = (1 - self.alpha) * current_q + self.alpha * target_q

        # 衰减探索率和学习率
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        self.alpha = max(0.01, self.alpha * self.alpha_decay)

    def train(self, episodes, max_steps=1000):
        """
        训练循环
        """
        rewards_history = []

        for episode in range(1, episodes + 1):
            state, _ = self.env.reset()
            total_reward = 0

            for step in range(max_steps):
                # 选择并执行动作
                action = self.get_action(state)
                next_state, reward, done, _, _ = self.env.step(action)

                # 更新Q-table
                self.update(state, action, reward, next_state, done)

                state = next_state
                total_reward += reward

                if done:
                    break

            rewards_history.append(total_reward)

            # 打印训练进度
            if episode % 10 == 0:
                avg_reward = np.mean(rewards_history[-10:])
                print(
                    f"Episode: {episode}, Avg Reward: {avg_reward:.2f}, Epsilon: {self.epsilon:.3f}, Alpha: {self.alpha:.3f}")

        return rewards_history