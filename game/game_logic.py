from .chess_board import ChessBoard


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
            
            # Check for game over conditions
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