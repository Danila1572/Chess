class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.value = 0
        
    def get_possible_moves(self, board):
        return []
    
    def move(self, new_position):
        self.position = new_position
        self.has_moved = True
        
    def __str__(self):
        return f"{self.color[0]}{self.__class__.__name__[0]}"


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.value = 1
        
    def get_possible_moves(self, board):
        moves = []
        x, y = self.position
        direction = -1 if self.color == 'white' else 1
        
        if 0 <= y + direction < 8 and board.get_piece((x, y + direction)) is None:
            moves.append((x, y + direction))

            if not self.has_moved and board.get_piece((x, y + 2*direction)) is None:
                moves.append((x, y + 2*direction))
        
        for dx in [-1, 1]:
            new_x, new_y = x + dx, y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = board.get_piece((new_x, new_y))
                if piece is not None and piece.color != self.color:
                    moves.append((new_x, new_y))
        
        return moves


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.value = 5
        
    def get_possible_moves(self, board):
        moves = []
        x, y = self.position
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                new_x, new_y = x + i*dx, y + i*dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = board.get_piece((new_x, new_y))
                    if piece is None:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break
                else:
                    break
                    
        return moves


class Horse(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.value = 3
        
    def get_possible_moves(self, board):
        moves = []
        x, y = self.position
        
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = board.get_piece((new_x, new_y))
                if piece is None or piece.color != self.color:
                    moves.append((new_x, new_y))
                    
        return moves


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.value = 3
        
    def get_possible_moves(self, board):
        moves = []
        x, y = self.position
        
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_x, new_y = x + i*dx, y + i*dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = board.get_piece((new_x, new_y))
                    if piece is None:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break
                else:
                    break
                    
        return moves


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.value = 9
        
    def get_possible_moves(self, board):
        rook = Rook(self.color, self.position)
        bishop = Bishop(self.color, self.position)
        return rook.get_possible_moves(board) + bishop.get_possible_moves(board)


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.value = 100
        
    def get_possible_moves(self, board):
        moves = []
        x, y = self.position
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = board.get_piece((new_x, new_y))
                    if piece is None or piece.color != self.color:
                        moves.append((new_x, new_y))
        
        return moves