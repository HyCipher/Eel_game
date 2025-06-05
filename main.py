# main.py

from env.canvas import Canvas
import pygame
import env.canvas as canvas
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
        player.update(canvas.width, canvas.height)
        player.draw(canvas.screen)

        # --- Fishes ---
        for fish in canvas.left_fishes:
            fish.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom)
            fish.draw(canvas.screen)

        for fish in canvas.right_fishes:
            fish.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom)
            fish.draw(canvas.screen)

        # --- Eels ---
        for eel in canvas.left_eels + canvas.right_eels:
            eel.update(canvas.width, canvas.height, wall_x, gap_top, gap_bottom, canvas.line_width)
            eel.draw(canvas.screen)

            # 电场作用检测
            for fish in canvas.left_fishes + canvas.right_fishes:
                if eel.affects(fish, wall_x):
                    fish.react_to_electric_field()

        pygame.display.flip()

    canvas.close()


def main():
    canvas = Canvas()
    run(canvas)


if __name__ == "__main__":
    main()
