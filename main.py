import pygame
from env.canvas import Canvas
import interaction.fish_catching as ifc
import interaction.eel_config as iec
from interaction import reward
from obj.player import Player
from interaction.eel_config import maybe_swap_eel_properties, is_swapped
from utils.logger import log_game_round


MAX_ROUNDS = 10  # 游戏轮数限制

def run(canvas):
    round_count = 0
    running = True

    while running and round_count < MAX_ROUNDS:

        # 初始化玩家
        player = Player(x=canvas.width // 2, y=canvas.height // 2)
        canvas.reset()  # 重置鱼和鳗鱼

        round_active = True  # 当前轮是否进行中

        while round_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    round_active = False

            canvas.screen.fill(canvas.background_color)
            canvas.wall.draw(canvas.screen)
            wall_x, gap_top, gap_bottom = canvas.wall.get_gap_bounds()

            # 玩家更新与绘制
            player.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, canvas.line_width)
            player.draw(canvas.screen)

            # 更新并绘制鱼
            for fish in canvas.left_fishes:
                fish.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, player)
                fish.draw(canvas.screen)
            for fish in canvas.right_fishes:
                fish.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, player)
                fish.draw(canvas.screen)

            # 更新并绘制鳗鱼
            for eel in canvas.left_eels + canvas.right_eels:
                eel.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, canvas.line_width)
                eel.draw(canvas.screen)

                # 电场作用
                for fish in canvas.left_fishes + canvas.right_fishes:
                    if eel.affects(fish, wall_x):
                        fish.react_to_electric_field(eel.slow_factor)

            # 检查 eel 激活（玩家是否触碰 eel）
            all_fishes = canvas.left_fishes + canvas.right_fishes
            all_eels = canvas.left_eels + canvas.right_eels
            result = ifc.check_eel_activation(player, all_eels, all_fishes, wall_x)

            if result:
                captured, eel_side = result

                # 移除捕获的鱼
                for fish in captured:
                    if fish in canvas.left_fishes:
                        canvas.left_fishes.remove(fish)
                    elif fish in canvas.right_fishes:
                        canvas.right_fishes.remove(fish)

                # 结果判定
                # 根据捕获数判定是否给奖励
                got_reward = reward.evaluate_reward(len(captured), eel_side)

                # 每轮结束后判断对调 eel 的属性
                maybe_swap_eel_properties()

                # 日志记录
                log_game_round(
                    round_number=round_count + 1,
                    eel_side=eel_side,
                    captured_count=len(captured),
                    got_reward=got_reward,
                    eel_config=iec.get_eel_properties(eel_side),
                    swapped=is_swapped()  # 记录是否对调
                )

                # 显示游戏结果
                # ifc.handle_game_over(captured, eel_side, round_count + 1, swapped)

                round_active = False  # 当前轮结束
                round_count += 1      # 进入下一轮

            pygame.display.flip()

    canvas.close()


def main():
    canvas = Canvas()
    run(canvas)


if __name__ == "__main__":
    main()
