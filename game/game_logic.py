import json
import os
from datetime import datetime
from .chess_board import ChessBoard
from .chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.selected_piece = None
        self.possible_moves = []
        self.game_over = False
        self.winner = None
        
    def select_piece(self, position):
        x, y = position
        if not (0 <= x < 8 and 0 <= y < 8):
            return False
            
        piece = self.board.get_piece(position)
        if piece is not None and piece.color == self.board.current_player:
            self.selected_piece = position
            self.possible_moves = piece.get_possible_moves(self.board)
            return True
        return False
        
    def move_selected_piece(self, to_position):
        if self.selected_piece is None:
            return False
            
        success = self.board.move_piece(self.selected_piece, to_position)
        if success:
            self.selected_piece = None
            self.possible_moves = []
            
            if self.board.is_checkmate('white'):
                self.game_over = True
                self.winner = 'black'
            elif self.board.is_checkmate('black'):
                self.game_over = True
                self.winner = 'white'
                
            return True
        return False
        
    def get_game_state(self):
        return {
            'board': self.board,
            'current_player': self.board.current_player,
            'selected_piece': self.selected_piece,
            'possible_moves': self.possible_moves,
            'game_over': self.game_over,
            'winner': self.winner,
            'captured_white': self.board.captured_pieces['white'],
            'captured_black': self.board.captured_pieces['black']
        }

    def save_game(self, slot=1):
        save_data = {
            'metadata': {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'current_player': self.board.current_player,
                'game_over': self.game_over,
                'winner': self.winner
            },
            'board': self._get_board_state(),
            'captured': {
                'white': [str(p) for p in self.board.captured_pieces['white']],
                'black': [str(p) for p in self.board.captured_pieces['black']]
            },
            'history': self.board.move_history,
            'game_state': {
                'selected_piece': self.selected_piece,
                'possible_moves': self.possible_moves
            }
        }
        
        os.makedirs('saves', exist_ok=True)
        with open(f'saves/save_{slot}.json', 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        return True
    
    def _get_board_state(self):
        board_state = []
        for y in range(8):
            row = []
            for x in range(8):
                piece = self.board.board[y][x]
                if piece:
                    row.append({
                        'type': piece.get_type(),
                        'color': piece.color,
                        'position': (x, y),
                        'has_moved': piece.has_moved
                    })
                else:
                    row.append(None)
            board_state.append(row)
        return board_state
    
    def load_game(self, slot=1):
        try:
            with open(f'saves/save_{slot}.json', 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.__init__()
            
            for y in range(8):
                for x in range(8):
                    piece_data = save_data['board'][y][x]
                    if piece_data:
                        self._restore_piece(piece_data)
            
            for color in ['white', 'black']:
                for piece_str in save_data['captured'][color]:
                    self._restore_captured_piece(piece_str, color)
            
            self.board.current_player = save_data['metadata']['current_player']
            self.board.move_history = save_data['history']
            self.game_over = save_data['metadata']['game_over']
            self.winner = save_data['metadata']['winner']
            self.selected_piece = save_data['game_state']['selected_piece']
            self.possible_moves = save_data['game_state']['possible_moves']
            
            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False
    
    def _restore_piece(self, piece_data):
        x, y = piece_data['position']
        color = piece_data['color']
        piece_type = piece_data['type']
        
        if piece_type == 'p': piece = Pawn(color, (x, y))
        elif piece_type == 'r': piece = Rook(color, (x, y))
        elif piece_type == 'h': piece = Knight(color, (x, y))
        elif piece_type == 'b': piece = Bishop(color, (x, y))
        elif piece_type == 'q': piece = Queen(color, (x, y))
        elif piece_type == 'k': piece = King(color, (x, y))
        
        piece.has_moved = piece_data['has_moved']
        self.board.board[y][x] = piece
    
    def _restore_captured_piece(self, piece_str, by_color):
        color = 'white' if piece_str[0] == 'w' else 'black'
        piece_type = piece_str[1].lower()
        
        if piece_type == 'p': piece = Pawn(color, (0, 0))
        elif piece_type == 'r': piece = Rook(color, (0, 0))
        elif piece_type == 'h': piece = Knight(color, (0, 0))
        elif piece_type == 'b': piece = Bishop(color, (0, 0))
        elif piece_type == 'q': piece = Queen(color, (0, 0))
        elif piece_type == 'k': piece = King(color, (0, 0))
        
        self.board.captured_pieces[by_color].append(piece)
    
    def get_save_slots(self):
        slots = []
        for i in range(1, 6):
            slot_info = {'slot': i, 'exists': False}
            try:
                with open(f'saves/save_{i}.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    slot_info.update({
                        'exists': True,
                        'date': data['metadata']['date'],
                        'player': data['metadata']['current_player']
                    })
            except:
                pass
            slots.append(slot_info)
        return slots