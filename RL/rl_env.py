import pygame
import numpy as np
from gym import Env
from gym.spaces import Box, Discrete, Dict
from env.canvas import Canvas
from obj.player import Player
from interaction.fish_catching import check_eel_activation
from interaction import reward as reward_system
from interaction.eel_config import maybe_swap_eel_properties, swapped_reset


class EelGameEnv(Env):
    def __init__(self, render_mode=None):
        super(EelGameEnv, self).__init__()

        # 初始化游戏画布（会自动初始化所有实体）
        self.canvas = Canvas()
        self.player = Player()  # 使用Player中的player实例

        # 动作空间和观察空间保持不变...
        self.action_space = Discrete(4)  # 0:上, 1:下, 2:左, 3:右

        self.observation_space = Dict({
            "player": Box(low=0, high=max(self.canvas.width, self.canvas.height), shape=(4,)),
            "fishes": Box(low=0, high=max(self.canvas.width, self.canvas.height), shape=(20, 2)),
            "eels": Box(low=0, high=max(self.canvas.width, self.canvas.height), shape=(4, 2)),
            "wall": Box(low=0, high=self.canvas.height, shape=(3,))
        })

        self.render_mode = render_mode
        self.clock = pygame.time.Clock() if render_mode == "human" else None
        self.current_round = 0
        self.max_rounds = 10

    def reset(self, seed=None, options=None):
        # 使用canvas的reset方法重置所有实体
        self.canvas.reset()
        self.current_round = 0

        observation = self._get_observation()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, info

    def step(self, action):
        if not self.round_active or self.current_round >= self.max_rounds:
            raise ValueError("Episode已经结束，请先调用reset()")

        # 执行动作
        if action == 0:
            self.player.move_left()
        elif action == 1:
            self.player.move_right()

        # 更新游戏状态
        wall_x, gap_top, gap_bottom = self.canvas.wall.get_gap_bounds()
        self.player.update(self.canvas.width, self.canvas.height, wall_x, gap_top, gap_bottom, self.canvas.line_width)

        # 更新鱼和鳗鱼
        self._update_fishes(wall_x, gap_top, gap_bottom)
        self._update_eels(wall_x, gap_top, gap_bottom)

        # 检查捕获事件
        terminated, truncated, step_reward = self._check_catch_event(wall_x)

        # 获取观察值和info
        observation = self._get_observation()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, step_reward, terminated, truncated, info

    def _update_fishes(self, wall_x, gap_top, gap_bottom):
        for fish in self.canvas.left_fishes + self.canvas.right_fishes:
            fish.update(self.canvas.width, self.canvas.height, wall_x, gap_top, gap_bottom, self.player)

    def _update_eels(self, wall_x, gap_top, gap_bottom):
        for eel in self.canvas.left_eels + self.canvas.right_eels:
            eel.update(self.canvas.width, self.canvas.height, wall_x, gap_top, gap_bottom, self.canvas.line_width)
            for fish in self.canvas.left_fishes + self.canvas.right_fishes:
                if eel.affects(fish, wall_x):
                    fish.react_to_electric_field(eel.slow_factor)

    def _check_catch_event(self, wall_x):
        all_fishes = self.canvas.left_fishes + self.canvas.right_fishes
        all_eels = self.canvas.left_eels + self.canvas.right_eels
        result = check_eel_activation(self.player, all_eels, all_fishes, wall_x)

        if not result:
            return False, False, -0.01  # 小型时间惩罚

        captured, eel_side = result
        self._remove_captured_fish(captured)

        # 计算奖励
        got_reward = reward_system.evaluate_reward(len(captured), eel_side)
        maybe_swap_eel_properties()

        # 更新回合状态
        self.round_active = False
        self.current_round += 1
        terminated = self.current_round >= self.max_rounds

        return terminated, False, got_reward

    def _remove_captured_fish(self, captured):
        for fish in captured:
            if fish in self.canvas.left_fishes:
                self.canvas.left_fishes.remove(fish)
            elif fish in self.canvas.right_fishes:
                self.canvas.right_fishes.remove(fish)

    def _get_observation(self):
        wall_x, gap_top, gap_bottom = self.canvas.wall.get_gap_bounds()

        # 玩家状态
        player_state = np.array([self.player.x, self.player.y,
                                 self.player.velocity_x, self.player.velocity_y])

        # 鱼群状态 (左+右)
        fish_states = np.zeros((20, 2))  # 最多10条鱼(每条鱼x,y)
        for i, fish in enumerate(self.canvas.left_fishes[:10] + self.canvas.right_fishes[:10]):
            fish_states[i] = [fish.x, fish.y]

        # 鳗鱼状态 (左+右)
        eel_states = np.zeros((4, 2))  # 最多2条鳗鱼
        for i, eel in enumerate(self.canvas.left_eels[:2] + self.canvas.right_eels[:2]):
            eel_states[i] = [eel.x, eel.y]

        return {
            "player": player_state,
            "fishes": fish_states,
            "eels": eel_states,
            "wall": np.array([wall_x, gap_top, gap_bottom])
        }

    def _get_info(self):
        return {
            "round": self.current_round,
            "left_fish": len(self.canvas.left_fishes),
            "right_fish": len(self.canvas.right_fishes),
            "left_eel": len(self.canvas.left_eels),
            "right_eel": len(self.canvas.right_eels)
        }

    def render(self):
        if self.render_mode != "human":
            return

        self.canvas.screen.fill(self.canvas.background_color)
        self.canvas.wall.draw(self.canvas.screen)
        self.player.draw(self.canvas.screen)

        for fish in self.canvas.left_fishes + self.canvas.right_fishes:
            fish.draw(self.canvas.screen)

        for eel in self.canvas.left_eels + self.canvas.right_eels:
            eel.draw(self.canvas.screen)

        pygame.display.flip()
        self.clock.tick(60)

    def close(self):
        if self.render_mode == "human":
            pygame.quit()