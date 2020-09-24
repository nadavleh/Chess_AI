import ChessEngine # importing the ChessEngine file we are writing
# import numpy
import copy


class ChessAI:
    def __init__(self):
        # self.pieceValue = {'P': 10, 'R': 50, 'N': 30, 'B': 30, 'Q': 90, 'K': 900}
        self.pieceValue = {'P': 100, 'R': 500, 'N': 320, 'B': 330, 'Q': 900, 'K': 20000}
        self.pieceSquaresTables = {
		"bP" :(     
				 (0,  0,  0,  0,  0,  0,  0,  0),
				 (50, 50, 50, 50, 50, 50, 50, 50),
				 (10, 10, 20, 30, 30, 20, 10, 10),
				 (5,  5, 10, 25, 25, 10,  5,  5),
				 (0,  0,  0, 20, 20,  0,  0,  0),
				 (5, -5,-10,  0,  0,-10, -5,  5),
				 (5, 10, 10,-20,-20, 10, 10,  5),
				 (0,  0,  0,  0,  0,  0,  0,  0)
			),

         "wP" :(
				(0,  0,  0,  0,  0,  0,  0,  0),
				(5, 10, 10,-20,-20, 10, 10,  5),
				(5, -5,-10,  0,  0,-10, -5,  5),
				(0,  0,  0, 20, 20,  0,  0,  0),
				(5,  5, 10, 25, 25, 10,  5,  5),
				(10, 10, 20, 30, 30, 20, 10, 10), 
				(50, 50, 50, 50, 50, 50, 50, 50), 
				(0,  0,  0,  0,  0,  0,  0,  0)
			),

         "bN" :(
				(-50,-40,-30,-30,-30,-30,-40,-50),
				(-40,-20,  0,  0,  0,  0,-20,-40),
				(-30,  0, 10, 15, 15, 10,  0,-30),
				(-30,  5, 15, 20, 20, 15,  5,-30),
				(-30,  0, 15, 20, 20, 15,  0,-30),
				(-30,  5, 10, 15, 15, 10,  5,-30),
				(-40,-20,  0,  5,  5,  0,-20,-40),
				(-50,-40,-30,-30,-30,-30,-40,-50)
			),

         "wN" :(
				(-50,-40,-30,-30,-30,-30,-40,-50),
				(-40,-20,  0,  5,  5,  0,-20,-40),
				(-30,  5, 10, 15, 15, 10,  5,-30),
				(-30,  0, 15, 20, 20, 15,  0,-30),
				(-30,  5, 15, 20, 20, 15,  5,-30),
				(-30,  0, 10, 15, 15, 10,  0,-30),
				(-40,-20,  0,  0,  0,  0,-20,-40),
				(-50,-40,-30,-30,-30,-30,-40,-50)
			),

         "bB" :( 
				(-20,-10,-10,-10,-10,-10,-10,-20),
				(-10,  0,  0,  0,  0,  0,  0,-10),
				(-10,  0,  5, 10, 10,  5,  0,-10),
				(-10,  5,  5, 10, 10,  5,  5,-10),
				(-10,  0, 10, 10, 10, 10,  0,-10),
				(-10, 10, 10, 10, 10, 10, 10,-10),
				(-10,  5,  0,  0,  0,  0,  5,-10),
				(-20,-10,-10,-10,-10,-10,-10,-20)
			),

         "wB" :( 
				(-20,-10,-10,-10,-10,-10,-10,-20),
				(-10,  5,  0,  0,  0,  0,  5,-10),
				(-10, 10, 10, 10, 10, 10, 10,-10),
				(-10,  0, 10, 10, 10, 10,  0,-10),
				(-10,  5,  5, 10, 10,  5,  5,-10),
				(-10,  0,  5, 10, 10,  5,  0,-10),
				(-10,  0,  0,  0,  0,  0,  0,-10),
				(-20,-10,-10,-10,-10,-10,-10,-20)
			),

         "bR" :( 
				(0,  0,  0,  0,  0,  0,  0,  0),
				(5, 10, 10, 10, 10, 10, 10,  5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
				(0,  0,  0,  5,  5,  0,  0,  0)
			),

         "wR" :( 
				(0,  0,  0,  5,  5,  0,  0,  0),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
			   (-5,  0,  0,  0,  0,  0,  0, -5),
				(5, 10, 10, 10, 10, 10, 10,  5),
				(0,  0,  0,  0,  0,  0,  0,  0)
			),

         "bQ" :( 
				(-20,-10,-10, -5, -5,-10,-10,-20),
				(-10,  0,  0,  0,  0,  0,  0,-10),
				(-10,  0,  5,  5,  5,  5,  0,-10),
				 (-5,  0,  5,  5,  5,  5,  0, -5),
				  (0,  0,  5,  5,  5,  5,  0, -5),
				(-10,  5,  5,  5,  5,  5,  0,-10),
				(-10,  0,  5,  0,  0,  0,  0,-10),
				(-20,-10,-10, -5, -5,-10,-10,-20)
			),

         "wQ" :( 
				(-20,-10,-10, -5, -5,-10,-10,-20),
				(-10,  0,  5,  0,  0,  0,  0,-10),
				(-10,  5,  5,  5,  5,  5,  0,-10),
				 (0,  0,  5,  5,  5,  5,  0, -5),
				(-5,  0,  5,  5,  5,  5,  0, -5),
				(-10,  0,  5,  5,  5,  5,  0,-10),
				(-10,  0,  0,  0,  0,  0,  0,-10),
				(-20,-10,-10, -5, -5,-10,-10,-20)
			  ),
		  
		  
		 "bK" :(  # the same as bKMiddleGame, this is just to simplify
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-20,-30,-30,-40,-40,-30,-30,-20),
				(-10,-20,-20,-20,-20,-20,-20,-10),
				 (20, 20,  0,  0,  0,  0, 20, 20),
				 (20, 30, 10,  0,  0, 10, 30, 20)
			),

         "wK" :( # the same as wKMiddleGame, this is just to simplify
				(20, 30, 10,  0,  0, 10, 30, 20),
				(20, 20,  0,  0,  0,  0, 20, 20),
				(-10,-20,-20,-20,-20,-20,-20,-10),
				(-20,-30,-30,-40,-40,-30,-30,-20),
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-30,-40,-40,-50,-50,-40,-40,-30),
				(-30,-40,-40,-50,-50,-40,-40,-30)   
			)
         }
        
        
        
    def getBestMove(self, position, depth = 3):
    # =============================================================================
    # this function is essentially a minimax algoithm implementatiom
    # =============================================================================
        # position is a gameState object (or rather a reference to one)
        if depth == 0 or position.checkmate or position.stalemate:
            return (self.staticPositionValue(position), None)
        else:
            if position.WhiteToMove:
                bestScore = -float("inf")
                bestMove = None
                validMoves = position.getValidMoves()
                for move in validMoves:
                    new_position = copy.deepcopy(position)
                    new_position.makeMove(move)
                    score, foo = self.getBestMove(new_position,depth-1)
                    if score > bestScore:
                        bestScore = score
                        bestMove = move
                return (bestScore, bestMove)
            else:
                bestScore = float("inf")
                bestMove = None
                validMoves = position.getValidMoves()
                for move in validMoves:
                    new_position = copy.deepcopy(position)
                    new_position.makeMove(move)
                    score, foo = self.getBestMove(new_position,depth-1)
                    if score < bestScore:
                        bestScore = score
                        bestMove = move
                return (bestScore, bestMove)

    def alphaBeta(self, position, depth = 3 , alpha = -float("inf"), beta = float("inf")):
        # print("entered at depth =", depth)
    # =============================================================================
    # this function is a minimax algoithm implementatiom with alpha-beta prunning
    # =============================================================================
        # position is a gameState object (or rather a reference to one)
        if depth == 0 or position.checkmate or position.stalemate:
            return (self.staticPositionValue(position), None)
        else:
            if position.WhiteToMove:
                bestMove = None
                validMoves = position.getValidMoves()
                for move in validMoves:
                    position.makeMove(move)
                    score, foo = self.alphaBeta(position,depth-1)
                    position.undoMove()
                    if score > alpha:
                        alpha = score
                        bestMove = move
                        if alpha >= beta:
                            print("prunning occured w")
                            break
                return (alpha, bestMove)
            else:
                bestMove = None
                validMoves = position.getValidMoves()
                for move in validMoves:
                    position.makeMove(move)
                    score, foo = self.alphaBeta(position,depth-1)
                    position.undoMove()
                    if score < beta:
                        beta = score
                        bestMove = move
                        if alpha >= beta:
                            print("prunning occured b")
                            break
                return (beta, bestMove)
    
    def staticPositionValue(self, gameState):
    # =============================================================================
    # this function is evaluates a position given in gameState.board by summing all the pieces values
    # (blacks values are the same as whites but negated) aswell as summing the square values of each respected 
    # piece, available in the pieceSquaresTables dictionary
    # =============================================================================
        sum = 0
        if gameState.checkmate:
            if gameState.WhiteToMove:
                return float("inf")
            else:
                return -float("inf")
        elif gameState.stalemate:
            return 0
        for r in range(8):
            for c in range(8):
                if gameState.board[r][c][0] == 'w':
                    sum += self.pieceValue[ gameState.board[r][c][1] ]
                    sum += self.pieceSquaresTables[ gameState.board[r][c] ][r][c]
                    
                elif gameState.board[r][c][0] == 'b':
                    sum -= self.pieceValue[ gameState.board[r][c][1] ]
                    sum -= self.pieceSquaresTables[ gameState.board[r][c] ][r][c]

        return sum                    
                    
                
        
        
        
        
        
        
        
        
        
        
            # self.pieceValue = {'P': 100, 'R': 500, 'N': 320, 'B': 330, 'Q': 900, 'K': 20000}
    
        
        
    # def alphaBeta(self, position, depth = 3 , alpha = -float("inf"), beta = float("inf")):
    #     # position is a gameState object (or rather a reference to one)
    #     if depth == 0 or position.checkmate or position.stalemate:
    #         return (self.staticPositionValue(position), None)
    #     else:
    #         if position.WhiteToMove:
    #             bestMove = None
    #             validMoves = position.getValidMoves()
    #             for move in validMoves:
    #                 new_position = copy.deepcopy(position)
    #                 new_position.makeMove(move)
    #                 score, foo = self.getBestMove(new_position,depth-1)
    #                 if score > alpha:
    #                     alpha = score
    #                     bestMove = move
    #                     if alpha >= beta:
    #                         break
    #             return (alpha, bestMove)
    #         else:
    #             bestMove = None
    #             validMoves = position.getValidMoves()
    #             for move in validMoves:
    #                 new_position = copy.deepcopy(position)
    #                 new_position.makeMove(move)
    #                 score, foo = self.getBestMove(new_position,depth-1)
    #                 if score < beta:
    #                     beta = score
    #                     bestMove = move
    #                     if alpha >= beta:
    #                         break
    #             return (beta, bestMove)
        

    # def getBestMove(self, position, depth = 3):
    #     # position is a gameState object (or rather a reference to one)
    #     if depth == 0 or position.checkmate or position.stalemate:
    #         return [self.staticPositionValue(position), None]
    #     else:
    #         if position.WhiteToMove:
    #             bestScore = -float("inf")
    #             bestMove = None
    #             validMoves = position.getValidMoves()
    #             for move in validMoves:
    #                 new_position = copy.deepcopy(position)
    #                 new_position.makeMove(move)
    #                 v = self.getBestMove(new_position,depth-1)
    #                 if v[0] > bestScore:
    #                     bestScore = v[0]
    #                     bestMove = v[1]
    #             return [bestScore, bestMove]
    #         else:
    #             bestScore = float("inf")
    #             bestMove = None
    #             validMoves = position.getValidMoves()
    #             for move in validMoves:
    #                 new_position = copy.deepcopy(position)
    #                 new_position.makeMove(move)
    #                 v = self.getBestMove(new_position,depth-1)
    #                 if v[0] < bestScore:
    #                     bestScore = v[0]
    #                     bestMove = v[1]
    #             return [bestScore, bestMove]
    









#     PAWN_TABLE = numpy.array([
#         [ 0,  0,  0,  0,  0,  0,  0,  0],
#         [ 5, 10, 10,-20,-20, 10, 10,  5],
#         [ 5, -5,-10,  0,  0,-10, -5,  5],
#         [ 0,  0,  0, 20, 20,  0,  0,  0],
#         [ 5,  5, 10, 25, 25, 10,  5,  5],
#         [10, 10, 20, 30, 30, 20, 10, 10],
#         [50, 50, 50, 50, 50, 50, 50, 50],
#         [ 0,  0,  0,  0,  0,  0,  0,  0]
#         ])
#     KNIGHT_TABLE = numpy.array([
#     [-50, -40, -30, -30, -30, -30, -40, -50],
#     [-40, -20,   0,   5,   5,   0, -20, -40],
#     [-30,   5,  10,  15,  15,  10,   5, -30],
#     [-30,   0,  15,  20,  20,  15,   0, -30],
#     [-30,   5,  15,  20,  20,  15,   0, -30],
#     [-30,   0,  10,  15,  15,  10,   0, -30],
#     [-40, -20,   0,   0,   0,   0, -20, -40],
#     [-50, -40, -30, -30, -30, -30, -40, -50]
# ])
#     BISHOP_TABLE = numpy.array([
#             [-20, -10, -10, -10, -10, -10, -10, -20],
#             [-10,   5,   0,   0,   0,   0,   5, -10],
#             [-10,  10,  10,  10,  10,  10,  10, -10],
#             [-10,   0,  10,  10,  10,  10,   0, -10],
#             [-10,   5,   5,  10,  10,   5,   5, -10],
#             [-10,   0,   5,  10,  10,   5,   0, -10],
#             [-10,   0,   0,   0,   0,   0,   0, -10],
#             [-20, -10, -10, -10, -10, -10, -10, -20]
#         ])    
#     ROOK_TABLE = numpy.array([
#             [ 0,  0,  0,  5,  5,  0,  0,  0],
#             [-5,  0,  0,  0,  0,  0,  0, -5],
#             [-5,  0,  0,  0,  0,  0,  0, -5],
#             [-5,  0,  0,  0,  0,  0,  0, -5],
#             [-5,  0,  0,  0,  0,  0,  0, -5],
#             [-5,  0,  0,  0,  0,  0,  0, -5],
#             [ 5, 10, 10, 10, 10, 10, 10,  5],
#             [ 0,  0,  0,  0,  0,  0,  0,  0]
#         ])    
#      QUEEN_TABLE = numpy.array([
#         [-20, -10, -10, -5, -5, -10, -10, -20],
#         [-10,   0,   5,  0,  0,   0,   0, -10],
#         [-10,   5,   5,  5,  5,   5,   0, -10],
#         [  0,   0,   5,  5,  5,   5,   0,  -5],
#         [ -5,   0,   5,  5,  5,   5,   0,  -5],
#         [-10,   0,   5,  5,  5,   5,   0, -10],
#         [-10,   0,   0,  0,  0,   0,   0, -10],
#         [-20, -10, -10, -5, -5, -10, -10, -20]
#     ])

    












