import pygame
import os
from pygame.locals import *
from game.game_logic import ChessGame


class ChessUI:
    def __init__(self):

        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Шахматы")
        
        self.cell_size = 60
        self.board_offset = (50, 50)
        
        self.game = ChessGame()
        self.load_images()
        self.font = pygame.font.SysFont('Arial', 24)
        
    def load_images(self):
        self.piece_images = {
            'Pw': pygame.image.load(os.path.join('assets', 'images', 'white_pawn.png')).convert_alpha(),
            'Rw': pygame.image.load(os.path.join('assets', 'images', 'white_rook.png')).convert_alpha(),
            'Nw': pygame.image.load(os.path.join('assets', 'images', 'white_horse.png')).convert_alpha(),
            'Bw': pygame.image.load(os.path.join('assets', 'images', 'white_bishop.png')).convert_alpha(),
            'Qw': pygame.image.load(os.path.join('assets', 'images', 'white_queen.png')).convert_alpha(),
            'Kw': pygame.image.load(os.path.join('assets', 'images', 'white_king.png')).convert_alpha(),
            'Pb': pygame.image.load(os.path.join('assets', 'images', 'black_pawn.png')).convert_alpha(),
            'Rb': pygame.image.load(os.path.join('assets', 'images', 'black_rook.png')).convert_alpha(),
            'Nb': pygame.image.load(os.path.join('assets', 'images', 'black_horse.png')).convert_alpha(),
            'Bb': pygame.image.load(os.path.join('assets', 'images', 'black_bishop.png')).convert_alpha(),
            'Qb': pygame.image.load(os.path.join('assets', 'images', 'black_queen.png')).convert_alpha(),
            'Kb': pygame.image.load(os.path.join('assets', 'images', 'black_king.png')).convert_alpha(),
        }
        self.board_image = pygame.image.load(os.path.join('assets', 'images', 'board.png')).convert_alpha()
        self.board_image = pygame.transform.scale(self.board_image, (self.cell_size * 8, self.cell_size * 8))
        
    def draw_board(self):
        self.screen.blit(self.board_image, self.board_offset)

        if self.game.selected_piece is not None:
            x, y = self.game.selected_piece
            rect = pygame.Rect(
                self.board_offset[0] + x * self.cell_size,
                self.board_offset[1] + (7 - y) * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)
            
            for move in self.game.possible_moves:
                mx, my = move
                rect = pygame.Rect(
                    self.board_offset[0] + mx * self.cell_size,
                    self.board_offset[1] + (7 - my) * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)
        
        for y in range(8):
            for x in range(8):
                piece = self.game.board.get_piece((x, y))
                if piece is not None:
                    piece_key = f"{str(piece)[1]}{str(piece)[0].lower()}"
                    if piece_key in self.piece_images:
                        image = self.piece_images[piece_key]
                        image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
                        self.screen.blit(
                            image,
                            (
                                self.board_offset[0] + x * self.cell_size,
                                self.board_offset[1] + (7 - y) * self.cell_size
                            )
                        )
        
        self.draw_captured_pieces()
        
        status_text = f"Ход: {'Белые' if self.game.board.current_player == 'white' else 'Чёрные'}"
        if self.game.game_over:
            status_text = f"Игра окончена! Победили: {'Белые' if self.game.winner == 'white' else 'Чёрные'}"
        
        text_surface = self.font.render(status_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.board_offset[0], self.board_offset[1] + 8 * self.cell_size + 20))
        
    def draw_captured_pieces(self):
        white_x = self.board_offset[0] + 8 * self.cell_size + 20
        black_x = self.board_offset[0] + 8 * self.cell_size + 20
        y = self.board_offset[1]
        
        text_white = self.font.render("Белые взяли:", True, (255, 255, 255))
        self.screen.blit(text_white, (white_x, y))
        y += 30
        
        for i, piece in enumerate(self.game.board.captured_pieces['black']):
            piece_key = f"{str(piece)[1]}{str(piece)[0].lower()}"
            if piece_key in self.piece_images:
                image = self.piece_images[piece_key]
                image = pygame.transform.scale(image, (self.cell_size // 2, self.cell_size // 2))
                self.screen.blit(image, (white_x + (i % 8) * (self.cell_size // 2 + 5), y + (i // 8) * (self.cell_size // 2 + 5)))
        
        y = self.board_offset[1] + 200
        text_black = self.font.render("Чёрные взяли:", True, (255, 255, 255))
        self.screen.blit(text_black, (black_x, y))
        y += 30
        
        for i, piece in enumerate(self.game.board.captured_pieces['white']):
            piece_key = f"{str(piece)[1]}{str(piece)[0].lower()}"
            if piece_key in self.piece_images:
                image = self.piece_images[piece_key]
                image = pygame.transform.scale(image, (self.cell_size // 2, self.cell_size // 2))
                self.screen.blit(image, (black_x + (i % 8) * (self.cell_size // 2 + 5), y + (i // 8) * (self.cell_size // 2 + 5)))
        
    def handle_click(self, pos):
        if self.game.game_over:
            return
            
        x = (pos[0] - self.board_offset[0]) // self.cell_size
        y = 7 - (pos[1] - self.board_offset[1]) // self.cell_size
        
        if 0 <= x < 8 and 0 <= y < 8:
            if self.game.selected_piece is None:
                self.game.select_piece((x, y))
            else:
                if (x, y) in self.game.possible_moves:
                    self.game.move_selected_piece((x, y))
                else:
                    self.game.select_piece((x, y))
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
            
            self.screen.fill((50, 50, 50))
            self.draw_board()
            pygame.display.flip()
            
        pygame.quit()