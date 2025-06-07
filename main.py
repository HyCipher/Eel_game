# main.py

from env.canvas import Canvas
import pygame
import interaction.fish_catching as ifc
from obj.player import Player


def run(canvas):
    running = True

    # 初始化
    player = Player(x=canvas.width // 2, y=canvas.height // 2)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        canvas.screen.fill(canvas.background_color)

        canvas.wall.draw(canvas.screen)

        wall_x, gap_top, gap_bottom = canvas.wall.get_gap_bounds()

        # --- Player update & draw ---
        player.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, canvas.line_width)
        player.draw(canvas.screen)

        # --- Fishes ---
        # Fish in left pool
        for fish in canvas.left_fishes:
            fish.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, player)
            fish.draw(canvas.screen)

        # Fish in right pool
        for fish in canvas.right_fishes:
            fish.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, player)
            fish.draw(canvas.screen)

        # --- Eels ---
        # Eels in left and right
        for eel in canvas.left_eels + canvas.right_eels:
            eel.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, canvas.line_width)
            eel.draw(canvas.screen)

            # 电场作用检测
            for fish in canvas.left_fishes + canvas.right_fishes:
                if eel.affects(fish, wall_x):
                    fish.react_to_electric_field(eel.slow_factor)

        # Eel捕获逻辑
        all_fishes = canvas.left_fishes + canvas.right_fishes
        all_eels = canvas.left_eels + canvas.right_eels

        result = ifc.check_eel_activation(player, all_eels, all_fishes, wall_x)

        if result:
            captured, eel_side = result

            # 从对应鱼池中移除
            for fish in captured:
                if fish in canvas.left_fishes:
                    canvas.left_fishes.remove(fish)
                elif fish in canvas.right_fishes:
                    canvas.right_fishes.remove(fish)

            # 结束游戏，并传入 eel 所在侧
            ifc.handle_game_over(captured, eel_side)

        pygame.display.flip()

    canvas.close()


def main():
    canvas = Canvas()
    run(canvas)


if __name__ == "__main__":
    main()
