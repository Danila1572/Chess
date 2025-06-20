import pygame
import os
from pygame.locals import *
from game.game_logic import ChessGame


class ChessUI:
    def __init__(self):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Шахматы")
        
        self.cell_size = 60
        self.board_offset = (50, 50)
        
        self.game = ChessGame()
        self.in_menu = False
        self.current_menu = 'main'
        self.selected_option = 0
        self.save_slots = 5
        
        self.font = pygame.font.SysFont('Arial', 24)
        self.menu_font = pygame.font.SysFont('Arial', 36)
        self.slot_font = pygame.font.SysFont('Arial', 18)
        
        self.settings = {
            'visual': {
                'light_color': (240, 217, 181),
                'dark_color': (181, 136, 99),
                'show_hints': True,
                'piece_scale': 1.0
            },
            'sound': {
                'enabled': True,
                'volume': 0.5,
                'move_sound': 'default',
                'capture_sound': 'default'
            },
            'game': {
                'animation_speed': 1.0,
                'confirm_exit': True
            }
        }
        
        self.menu_options = {
            'main': ['Продолжить', 'Новая игра', 'Сохранить игру', 'Загрузить игру', 'Настройки', 'Выход'],
            'save': ['Слот 1', 'Слот 2', 'Слот 3', 'Слот 4', 'Слот 5', 'Назад'],
            'load': ['Слот 1', 'Слот 2', 'Слот 3', 'Слот 4', 'Слот 5', 'Назад'],
            'settings': [
                'Цвет светлых клеток',
                'Цвет темных клеток',
                f"Показывать подсказки: {'Вкл' if self.settings['visual']['show_hints'] else 'Выкл'}",
                f"Громкость звуков: {int(self.settings['sound']['volume'] * 100)}%",
                f"Анимация: {'Вкл' if self.settings['game']['animation_speed'] > 0 else 'Выкл'}",
                f"Подтверждение выхода: {'Вкл' if self.settings['game']['confirm_exit'] else 'Выкл'}",
                'Сброс настроек',
                'Назад'
            ]
        }
        
        self.load_images()

    def load_images(self):
        self.piece_images = {
            'Pw': pygame.image.load(os.path.join('assets', 'images', 'white_pawn.png')).convert_alpha(),
            'Rw': pygame.image.load(os.path.join('assets', 'images', 'white_rook.png')).convert_alpha(),
            'Hw': pygame.image.load(os.path.join('assets', 'images', 'white_knight.png')).convert_alpha(),
            'Bw': pygame.image.load(os.path.join('assets', 'images', 'white_bishop.png')).convert_alpha(),
            'Qw': pygame.image.load(os.path.join('assets', 'images', 'white_queen.png')).convert_alpha(),
            'Kw': pygame.image.load(os.path.join('assets', 'images', 'white_king.png')).convert_alpha(),
            'Pb': pygame.image.load(os.path.join('assets', 'images', 'black_pawn.png')).convert_alpha(),
            'Rb': pygame.image.load(os.path.join('assets', 'images', 'black_rook.png')).convert_alpha(),
            'Hb': pygame.image.load(os.path.join('assets', 'images', 'black_knight.png')).convert_alpha(),
            'Bb': pygame.image.load(os.path.join('assets', 'images', 'black_bishop.png')).convert_alpha(),
            'Qb': pygame.image.load(os.path.join('assets', 'images', 'black_queen.png')).convert_alpha(),
            'Kb': pygame.image.load(os.path.join('assets', 'images', 'black_king.png')).convert_alpha(),
        }
        
        board_img_path = os.path.join('assets', 'images', 'board.png')
        if os.path.exists(board_img_path):
            self.board_image = pygame.image.load(board_img_path).convert_alpha()
            self.board_image = pygame.transform.scale(self.board_image, 
                                                   (self.cell_size * 8, self.cell_size * 8))
        else:
            self.board_image = pygame.Surface((self.cell_size * 8, self.cell_size * 8))
            self.board_image.fill((0, 0, 0))

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
    
    def draw_menu(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        if self.current_menu == 'settings':
            self.draw_settings()
        else:
            title = self.menu_font.render(
                'Меню' if self.current_menu == 'main' else 
                'Сохранение игры' if self.current_menu == 'save' else 
                'Загрузка игры', True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.screen_width//2, self.screen_height//4))
            self.screen.blit(title, title_rect)
            
            options = self.menu_options[self.current_menu]
            for i, option in enumerate(options):
                color = (255, 215, 0) if i == self.selected_option else (255, 255, 255)
                
                if self.current_menu in ['save', 'load'] and i < self.save_slots:
                    save_info = self.game.get_save_slots()[i]
                    if save_info['exists']:
                        option_text = f"{option} ({save_info['date']})"
                        info_text = f"Ход: {'белых' if save_info['player'] == 'white' else 'черных'}"
                    else:
                        option_text = f"{option} (пусто)"
                        info_text = ""
                else:
                    option_text = option
                    info_text = ""
                
                text = self.menu_font.render(option_text, True, color)
                text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 + i*50))
                self.screen.blit(text, text_rect)
                
                if info_text:
                    info = self.slot_font.render(info_text, True, (200, 200, 200))
                    info_rect = info.get_rect(center=(self.screen_width//2, self.screen_height//2 + i*50 + 30))
                    self.screen.blit(info, info_rect)

    def handle_menu_input(self):
        keys = pygame.key.get_pressed()
        
        if self.current_menu == 'settings':
            self.handle_settings_input()
        else:
            if keys[pygame.K_DOWN]:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options[self.current_menu])
                pygame.time.delay(150)
            
            if keys[pygame.K_UP]:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options[self.current_menu])
                pygame.time.delay(150)
                
            if keys[pygame.K_RETURN]:
                option = self.menu_options[self.current_menu][self.selected_option]
                
                if self.current_menu == 'main':
                    if option == 'Продолжить':
                        self.in_menu = False
                    elif option == 'Новая игра':
                        self.game = ChessGame()
                        self.in_menu = False
                    elif option == 'Сохранить игру':
                        self.current_menu = 'save'
                        self.selected_option = 0
                    elif option == 'Загрузить игру':
                        self.current_menu = 'load'
                        self.selected_option = 0
                    elif option == 'Настройки':
                        self.current_menu = 'settings'
                        self.selected_option = 0
                    elif option == 'Выход':
                        pygame.quit()
                        exit()
                
                elif self.current_menu == 'save':
                    if option == 'Назад':
                        self.current_menu = 'main'
                        self.selected_option = 2
                    elif self.selected_option < self.save_slots:
                        if self.game.save_game(self.selected_option + 1):
                            self.current_menu = 'main'
                            self.selected_option = 0
                
                elif self.current_menu == 'load':
                    if option == 'Назад':
                        self.current_menu = 'main'
                        self.selected_option = 3
                    elif self.selected_option < self.save_slots:
                        if self.game.load_game(self.selected_option + 1):
                            self.in_menu = False
                        else:
                            print("Не удалось загрузить игру")
        
        if keys[pygame.K_ESCAPE]:
            if self.current_menu == 'main':
                self.in_menu = False
            else:
                self.current_menu = 'main'
                self.selected_option = 0
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.in_menu = not self.in_menu
                        if self.in_menu:
                            self.current_menu = 'main'
                            self.selected_option = 0
                    elif self.in_menu:
                        self.handle_menu_input()
                elif event.type == MOUSEBUTTONDOWN and not self.in_menu:
                    if event.button == 1:
                        self.handle_click(event.pos)
            
            self.screen.fill((50, 50, 50))
            self.draw_board()
            
            if self.in_menu:
                self.draw_menu()
            
            pygame.display.flip()
        
        pygame.quit()