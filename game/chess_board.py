from .chess_pieces import Pawn, Rook, Horse, Bishop, Queen, King


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.current_player = 'white'
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        
    def setup_board(self):
        for i in range(8):
            self.board[1][i] = Pawn('black', (i, 1))
            self.board[6][i] = Pawn('white', (i, 6))
            
        self.board[0][0] = Rook('black', (0, 0))
        self.board[0][7] = Rook('black', (7, 0))
        self.board[7][0] = Rook('white', (0, 7))
        self.board[7][7] = Rook('white', (7, 7))
        
        self.board[0][1] = Horse('black', (1, 0))
        self.board[0][6] = Horse('black', (6, 0))
        self.board[7][1] = Horse('white', (1, 7))
        self.board[7][6] = Horse('white', (6, 7))
        
        self.board[0][2] = Bishop('black', (2, 0))
        self.board[0][5] = Bishop('black', (5, 0))
        self.board[7][2] = Bishop('white', (2, 7))
        self.board[7][5] = Bishop('white', (5, 7))
        
        self.board[0][3] = Queen('black', (3, 0))
        self.board[7][3] = Queen('white', (3, 7))
        
        self.board[0][4] = King('black', (4, 0))
        self.board[7][4] = King('white', (4, 7))
        
    def get_piece(self, position):
        x, y = position
        return self.board[y][x]
    
    def move_piece(self, from_pos, to_pos):
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        piece = self.board[from_y][from_x]
        if piece is None:
            return False
            
        if piece.color != self.current_player:
            return False
            
        if to_pos not in piece.get_possible_moves(self):
            return False
            
        target_piece = self.board[to_y][to_x]
        if target_piece is not None:
            self.captured_pieces[target_piece.color].append(target_piece)
            
        self.board[to_y][to_x] = piece
        self.board[from_y][from_x] = None
        piece.move(to_pos)
        
        self.move_history.append((from_pos, to_pos))
        
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
        
    def is_check(self, color):
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos is not None:
                break
                
        if king_pos is None:
            return False
            
        opponent_color = 'black' if color == 'white' else 'white'
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color == opponent_color:
                    if king_pos in piece.get_possible_moves(self):
                        return True
                        
        return False
        
    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
            
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color == color:
                    for move in piece.get_possible_moves(self):
                        original_piece = self.board[move[1]][move[0]]
                        original_pos = piece.position
                        
                        self.board[move[1]][move[0]] = piece
                        self.board[y][x] = None
                        piece.position = move
                        
                        still_in_check = self.is_check(color)
                        
                        self.board[move[1]][move[0]] = original_piece
                        self.board[y][x] = piece
                        piece.position = original_pos
                        
                        if not still_in_check:
                            return False
                            
        return True
        
    def __str__(self):
        board_str = ""
        for row in reversed(self.board):
            board_str += " ".join([str(piece) if piece is not None else ".." for piece in row]) + "\n"
        return board_str