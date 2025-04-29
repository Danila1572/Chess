import pygame
import os

os.makedirs('assets/images', exist_ok=True)

pygame.init()

board_size = 480
cell_size = board_size // 8

board_surface = pygame.Surface((board_size, board_size))

light_color = (240, 217, 181)
dark_color = (181, 136, 99)

for y in range(8):
    for x in range(8):
        color = light_color if (x + y) % 2 == 0 else dark_color
        pygame.draw.rect(
            board_surface,
            color,
            (x * cell_size, y * cell_size, cell_size, cell_size)
        )

pygame.image.save(board_surface, 'assets/images/board.png')
print

pygame.quit()