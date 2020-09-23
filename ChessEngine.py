class GameState():
    
    def __init__(self):

        self.board =[  #consider switching to np array                                        
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]            
            ]
        
        
        # self.board =[  #consider switching to np array                                        
        #     ["bR", "--","--", "--", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "--", "--", "--", "wK", "wB", "wN", "wR"]            
        #     ]
        
        
        
        
        self.WhiteToMove = True
        self.MoveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.isCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.sideWon = '--'
        self.enPassant  = [False, 'w', 4] # this is a list indicating the following: [if an en-passant move is possible, 
                                          # what color can preform the enpassant, on which file\collumn it is to be made]
                                          
        ################################ castling variables ######################################                                
        # inorder to reverse a king move we need to keep track of how many moves i has made, just a simple boolean var
        # is not enough. e.g. if we set such a bool var self.hasWhiteKingRookMoved = True once the white king has moved,
        # if the player would want to undo that move, we need to revece this var to False so that the player can castle 
        # instead or in the future. However if it wasnt the kings first move (he may have moved previously, to an adjacent square
        # and came back a turn later) then setting the var to False would indicate the king hasnt moved previously and that 
        # castling may be permitted. And so, we track the num of king moves and allow casling iff num_of_king_moves == 0        
        self.whiteKingMoveCount = 0
        self.blackKingMoveCount = 0
        # the same move counting needs to be done with the rooks, as casling is prohibitted with a rook that has previously travelled.
        #  however this is more problematic becausehow do we keep track of the rooks during the game? how do we know which rook is a quenside rook 
        # or a kingside rook in the middlegame? we can track their movements but that will cost us space and time, so we will just increment
        # these counters when a rook leaes its original square, and decrement it if the player undoes a move which had a rook returning to one 
        # of the two original rook positions. That will almost surely keep these counters at 0 aslong as the corresponding rooks hasnt moved
        # !!!!Attention!!!!: keep in mind that this alg' may present bugs in the middle game if alot of undoes have occured and the rooks shufled somehow to the
        # original square
        self.whiteKingsideRookMoveCount = 0
        self.blackKingsideRookMoveCount = 0
        self.whiteQueensideRookMoveCount = 0
        self.blackQueensideRookMoveCount = 0
        #########################################################################################
        self.moveFunctions = {'P': self.getPawnMoves, 'B': self.getBishopMoves, 'N': self.getKnightMoves,
                              'R': self.getRookMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves }
        
    def makeMove(self, move):
        # print("white kingside rook num of moves:", self.whiteKingsideRookMoveCount)
        # print("piece moved from",(move.startRow,move.startCol) )
        
        # recive a class "Move" object "move"
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.MoveLog.append(move)
        allyColor = "w" if self.WhiteToMove else "b"
        ###############################   Castling   ##########################################  
        # prevent casling if the rook moved before casling. Attention: this var !!isn't!! changed to true after castling, but only the "hasWhite\BlackKingMoved"
        # var is changed and inticates castling is prohibitted
        if move.pieceMoved[1] == 'R' and self.WhiteToMove and (move.startRow,move.startCol) == (7,7):
            # self.hasWhiteKingRookMoved = True
            self.whiteKingsideRookMoveCount += 1
        elif move.pieceMoved[1] == 'R' and not self.WhiteToMove and (move.startRow,move.startCol) == (0,7):
            # self.hasBlackKingRookMoved = True  
            self.blackKingsideRookMoveCount += 1
        if move.pieceMoved[1] == 'R' and self.WhiteToMove and (move.startRow,move.startCol) == (7,0):
            # self.hasWhiteQueenRookMoved = True
            self.whiteQueensideRookMoveCount += 1
        elif move.pieceMoved[1] == 'R' and not self.WhiteToMove and (move.startRow,move.startCol) == (0,0):
            # self.hasBlackQueenRookMoved = True 
            self.blackQueensideRookMoveCount += 1
        
        if move.isCastle:
            if move.isKingSideCastle:
                self.board[move.endRow][move.endCol-1] = allyColor+'R'
                self.board[move.endRow][move.endCol+1] ="--"
            else:  # castling queenside
                self.board[move.endRow][move.endCol+1] = allyColor+'R'
                self.board[move.endRow][move.endCol-2] ="--"                
   
        ###############################   En-Passant  #########################################  
        # check if a pawn that can be taken en-pass was just moved, and update the self.enPassant list accordingly
        # reminder: self.enPassant == [en-pass is possible flag, which side can take the pawn moved, on what col can this pawn be taken]
        if self.WhiteToMove and move.pieceMoved == "wP" and move.startRow == 6 and move.endRow == 4:
            self.enPassant = [True, 'b', move.endCol] 
        elif not self.WhiteToMove and move.pieceMoved == "bP" and move.startRow == 1 and move.endRow == 3:
            self.enPassant = [True, 'w', move.endCol]
        # In the getPawnMoves() funcion there's a condition which allows taking en-pass if  self.enPassant[0]==True and there's
        # a pawn that can be taken en-pass. in that case we append to the valid moves list the corresponding move, which is the only one
        # who has the flag move.enPassant==True. Thats how we can tell if an en-pass move is made, and remove the taken pawn.
        # (in en-pass the attacking pawn doesnt take the attacked pawn on the same square so it needs to be dealt with seperately)
        if move.enPassant:
            if move.endRow == 2: # its white who en-passed, remove the black pawn from the board
                self.board[move.startRow][move.endCol] = "--"
            else:                # its black who en-passed, remove the white pawn from the board
                self.board[move.startRow][move.endCol] = "--"
        # Allways turn off the en-passant flag after a move which is not a two step pawn move (the one that turn the flag to True) 
        if not( (move.pieceMoved == 'bP' and move.endRow == 3 ) or (move.pieceMoved == 'wP' and move.endRow == 4 ) ):
            self.enPassant[0] = False  
        
        ############################## pawn promotion move #################################### 
        # in order of easy implementation, we will automatically promote to a queen at this stage
        if move.isPawnPromotion:
             self.board[move.endRow][move.endCol] = move.pieceMoved[0]+"Q"   # automatically make the pawn a queen of the same color as
                                                                             # the pawn, the color is stored in move.pieceMoved[0] to which
                                                                             # we concatenate 'Q' for queen
        ####################################################################################### 
        self.WhiteToMove = not self.WhiteToMove
        # update kings location if its the piece that moved
        
        # if the KIng has moved or castled, update its location and indicate it has made a move (so that it cant castle anymore)
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
            self.whiteKingMoveCount += 1
            # if not move.isCastle:
            #     self.hasWhiteKingMoved = True
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)  
            self.blackKingMoveCount += 1
            # if not move.isCastle:
            #     self.hasBlackKingMoved = True
                
    def undoMove(self):
    # =============================================================================
    # this fnction undo's the last move by poping the last move from the moveLog list 
    # and jus reversing it i.e. setting the board to have the captured piece where it was
    # and the moving piece where it was
    # =============================================================================
        if len(self.MoveLog) != 0: 
            move = self.MoveLog.pop() # remember that the move log is a list of "Move" objects
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            ################### if it was an en-passant move #####################
            if move.enPassant:
                if move.startRow == 3: # it was white's pawn move
                    self.board[move.startRow][move.endCol] = 'bP'
                else:                  # it was black's pawn move
                    self.board[move.startRow][move.endCol] = 'wP'
            
            ################### if it was a pawn promotion  ######################
            # no need to consider that scenario! the function works well for pawn promo without any problems
            ###################    if it was castling      #######################
            if move.isCastle:
                allyColor = "w" if not self.WhiteToMove else "b"
                # restore the rook to its original position
                if move.isKingSideCastle: # the move was a kingside castle
                    self.board[move.endRow][move.endCol+1] = allyColor + 'R'
                    self.board[move.endRow][move.endCol-1] = "--"
                else:                     # the move was a queenside castle
                    self.board[move.endRow][move.endCol-2] = allyColor + 'R'
                    self.board[move.endRow][move.endCol+1] = "--"     
            # if it was a rook move and not castling, that move had incremented the self.<color><King\Queen>sideRook counter 
            # (e.g. the line "self.whiteKingsideRookMoveCount += 1" in the makeMove() function). Let's deal with this here
            # just because relevant only to casling (castle is posible only when the counter == 0 ) but how do we tell what rook it is?
            # i.e. is the rook moved is a queenside or a kingside rook? we are able to identify the rook based on its initial position
            # for example if the move was from the (7,7) square, its probably the white kingside rook (although during he game the rooks may change positions 
            # and these countes may get bugs if we decrease one of them by accident to 0, but its likely not gonna happen)
            # further more, its only relevant to decrease the counter when the rook left its initial square and got back to it in an undo, in that case
            # it means that he rook move may have been a first rook move, thus reversing it will set its counter to 0. if it wasnt the first rook move
            # then the counter will be greater than zero een if we decrease it by 1, and no castling can occure as the rules say (the rook must not hae moved prior to casling)
            if move.pieceMoved[1] == 'R' and not self.WhiteToMove and (move.startRow,move.startCol) == (7,7):
                # self.hasWhiteKingRookMoved = True
                self.whiteKingsideRookMoveCount -= 1
            elif move.pieceMoved[1] == 'R' and self.WhiteToMove and (move.startRow,move.startCol) == (0,7):
                # self.hasBlackKingRookMoved = True  
                self.blackKingsideRookMoveCount -= 1
            if move.pieceMoved[1] == 'R' and not self.WhiteToMove and (move.startRow,move.startCol) == (7,0):
                # self.hasWhiteQueenRookMoved = True
                self.whiteQueensideRookMoveCount -= 1
            elif move.pieceMoved[1] == 'R' and self.WhiteToMove and (move.startRow,move.startCol) == (0,0):
                # self.hasBlackQueenRookMoved = True 
                self.blackQueensideRookMoveCount -= 1
            

            ######################################################################
            self.WhiteToMove = not self.WhiteToMove #switch again the turns so its the "undoing side"'s turn once more
            
            # update kings location and move counter, if its the piece that moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
                self.whiteKingMoveCount -= 1
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
                self.blackKingMoveCount -= 1
    def getValidMoves(self):
    # =============================================================================
    # this function first calls self.checkForPinsAndChecks() to see if there are any pins or checks
    # and acts accordingly. e.g. if there is just one piece checking the playing king, the playing side
    # can block it\capture the checking piece\move the king, but if there are two pieces checking the king 
    # than simple logic states that the king must move because no block\capture can prevent both piecesw from checking the king.
    
    # this function is just a simple rules implementation, the real magic is in self.checkForPinsAndChecks().
    # reminder: 
    #   1) self.inCheck == a boolean variable indicating a check if True
    #   2) self.pins == a list containing tuples, each with 4 entries: (pinned piece row, pinned piece col, pinned piece direction row, pinned piece direction col )
    #   3) self.checks == a list containing tuples, each with 4 entries: (checking piece row, checking piece col, checking piece direction row, checking piece direction col )
    # =============================================================================

        moves = []
        
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        
        # get the playing side's king position 
        if self. WhiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: # only one check. Block it or move he king
                moves = self.getAllPossibleMoves()
                # print("number of valid moves: ",len(moves) )
                
                # to block a check you must move a piece into one of the squares between the attacking piece and the king
                check = self.checks[0] # there is only one checking piece thus it is at index 0 in the self.checks list
                checkRow = check[0] # the checking piece's row location
                checkCol = check[1] # the checking piece's collumn location
                pieceChecking = self.board[checkRow][checkCol] # get which of the enemy's pieces is checking he king
                validSquares = [] # squares that pieces can move to
                # if a knight is checking the king. you must capture the knight or move the king. theres no way of blocking this check
                if pieceChecking == 'N':
                    validSquares = [(checkRow,checkCol)]
                else: # the attacking piece is not a knight thus you can block it anywhere between the king and the piece itself
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) # check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0]==checkRow and validSquare[1]==checkCol: # once you get to piece, end checks
                            break
                # get rid of any moves that dont block the check or move the king
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K': # remove all non-king moves which are not blocking the check
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: # at least two pieces are attacking the king: double check, thus the king has to move
                self.getKingMoves(kingRow, kingCol, moves) 
            # =============================================================================
            # now if the moves list is empty then we are checkmated because no valid moves which block the check or move the king exists
            if len(moves)==0:
                self.checkmate = True
                self.sideWon  = 'b' if self.WhiteToMove else 'w'
            # =============================================================================
        else: # no checks so all moves are fine
            moves = self.getAllPossibleMoves()
            # =============================================================================
            # now if the moves list is empty then we are in stalemate because no valid moves exist, and we are not in check
            if len(moves)==0:
                self.stalemate = True
            # =============================================================================
        # self.WhichPiecesCanMove(moves)
        # print("is checkmate:",self.checkmate, "length of moves:", len(moves))
        return moves
    def checkForPinsAndChecks(self):
    # =============================================================================
    # the following function checks all direction around the playing side's king
    # for: 
    # 1) allied pieces + enemy pieces == possible pins: if it finds them it appends the piece and its direction to a possiblePins list
    #    and continues to check the same direction for other allied pieces (and then no checks of pins in that direction)
    #    or for ennemy attacking piece. in that case the ally piece must be pinned and the piece and its direction
    #    in which case the ally piece and its direction are appended to the self.pins list
    # 2) enemy pieces == possible checks: if an enemy piece is found in a certine directions and its a piece capable of attacking in that direction,
    #    then we check if theres a possible pin (if the possiblePins list is not empty) otherwise it must be a check
    # The function returns inCheck == boolean value indicating check , pins and checks == lists containing pinned or checking pieces locations and their direction relative to the king whose side's turn it is
    # =============================================================================
        pins = []            # this is a list of pieces pinned to the king?
        checks = []          # this is a list containing tuples of pieces checking the king e.g. a tuple : (piece row, piece col, directions[i][0], directions[i][1] (direction of piece) )
        inCheck = False      # this is a boolean indicator of check?
        
        # get the playing side's king position 
        if self.WhiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
            
        # go in either one of the following directions (all orthogonal and diagonal possibilities around the king)
        # and check if there's an enemy piece that threatens our king at (startRow,startCol)
        directions = ( (-1,0), (0,-1), (1,0), (0,1),   # idxs 0 to 3 are orthogonal directions
                      (-1,-1), (-1,1), (1,-1), (1,1) ) # idxs 4 to 7 are  diagonal directions
        
        for j in range(len(directions)): # for each direction in "directions"
             d = directions[j]
             possiblePin = ()
             for i in range(1,8): # go through all the squares in each direction (as long as they are on the board of course 0<=endRow<=7 and 0<=endCol<=7 )
                 endRow = startRow + d[0]*i
                 endCol = startCol + d[1]*i
                 if 0<=endRow<=7 and 0<=endCol<=7:
                     endPiece = self.board[endRow][endCol] # get the piece on that square (may be an empty square "--")
                     
                     # if we run into an ally piece, we need to check if it is pinned i.e. theres no other ally piece beyond
                     # it (in the same direction) and there is an enemy piece hreatenning in this direction, else it is not pinned
                     # we will use the "possiblePin" tuple to store pieces which stand in a cerrtain direction relative to the king
                     # and querrying whether they are pinned (is there an ally piece beond them? if not, are they and the king threatend by a bishop/rook/queen?)
                     if endPiece[0] == allyColor:
                         if possiblePin == (): # 1st allied piece we encounter in the d directions 
                             possiblePin = (endRow, endCol, d[0], d[1]) # store that piece's location and direction (relative to the king) in this tuple
                         else: 
                             break # we encountered a 2nd allied piece in the d direction so no pin nor check is possible in that direction
                             
                     # if the piece we encountered in that direction from the king is an enemy piece, we must see if the king
                     # is in check. first we retrieve the type of the enemy piece (Q\R\B\P\N\K)
                     elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # there are 5 possibilities in this complex conditional:
                        #1.) othogonally away from the king and piece is a rook: this is directions 0 to 3 in "directions"
                        #2.) diagonally away from king and piece is a bishop: this is directions 4 to 7 in "directions"
                        #3.) 1 square away diagonally from king and piece is a pawn
                        #4.) any direction and piece is a queen
                        #5.) any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        
                        # !.) note: (the dash '\' in the following if statement is the only way of dropping lines in python if statements https://stackoverflow.com/questions/53162/how-can-i-do-a-line-break-line-continuation-in-python)
                        if (0<=j<=3 and type == 'R') or \
                            (4<=j<=7 and type == 'B') or \
                            (i==1 and type == 'P' and ((enemyColor == 'w' and 6<=j<=7) or (enemyColor == 'b' and 4<=j<=5))) or\
                            (type == 'Q') or (i==1 and type =='K'): ## TODO:  i think the (i==1 and type =='K') 
                                                                    ## is unecessary because the kings cant check each other, 
                                                                    ## we prevent kings getting to close to each other in getKingMoves()
                                                                    ## however i dont remove it because it doesn matter.. it will never be True and its in an "or" statement, so we can always concatenate if something or False or False or.. and so on
                            if possiblePin == (): # no piece blocking so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # ally piece blocking checking piece so ally piece is pinned
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check so no othe piece can check or pin in this direction, so break the inner loop which searches this direction 
                            break
                 else:
                     break # endRow or endCol are the off board
        # check for knight checks. a night is an awed duck, so we verify its checks seperately
        knightMoves = ( (-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1) )                       
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0<=endRow<=7 and 0<=endCol<=7:
                endPiece = self.board[endRow][endCol]   
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # enemy knigh attecking te king
                    inCheck == True
                    checks.append( (endRow,endCol,m[0],m[1]) )
        return inCheck,pins,checks             
    def getAllPossibleMoves(self):
    # =============================================================================
    # this function itterates trough the board (8 by 8 nested loop). Once it lands on a square
    # on which a playing side's piece is at, it calls that piece's move generating function which appends
    # to the "moves" list, "Move" objects of all valid piece moves. the validity is veryfied through the
    # self.pins list and the normal rulls of that piece movements
    # =============================================================================
        moves = []
        for r in range(len(self.board)): #for each row in the board
            for c in range(len(self.board[r])): #for each square (column) in a row 
                turn = self.board[r][c][0] # get the first letter of the sring e.g. if board[r][c]="wP" then board[r][c][0] = w and we know what color the piece is
                if (turn=='w' and self.WhiteToMove) or (turn=='b' and not self.WhiteToMove): 
                    piece = self.board[r][c][1]   
                    self.moveFunctions[piece](r,c,moves)
        # self.WhichPiecesCanMove(moves)  # this is a debug function i wrote        
        return moves
    def WhichPiecesCanMove(self, moves):
        
    # =============================================================================
    # the following function counts haw many moves each piece can make 
    # =============================================================================
        movingPieces = {'P': 0, 'B': 0, 'N': 0,
                        'R': 0, 'Q': 0, 'K': 0 }
        for i in range(len(moves)):
            piss = moves[i].pieceMoved[1] # using piss instead of "piece" just so we dont have so many vars with the same name
            movingPieces[piss]+=1
        print(movingPieces)        
    def getPawnMoves(self, r,c, moves):        
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # itterate through the pinned pieces list and determine if the pawn 
                                                  # which we want to generate moves for, is a pinned piece or not.
                                                  # we itterate backwards to prevent possible bugs arrising from deleting an item from the list.
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i]) #why the hell should i remove a pin from the list it just takes alot of time updating the list (done in the backround but still..)
                break
        # white pawn movement
        if self.WhiteToMove:
            ###############################  white En-Passant  #########################################  
            # if enpassant is possible AND the color to move is white AND the pawn in question is on either side of the black pawn which just moved:
            if self.enPassant[0] and self.enPassant[1] == 'w' and r==3 and ( c==(self.enPassant[2]+1) or c==(self.enPassant[2]-1) ):
                # verify that the pawn is not pinned or that its en-passing in the direction of the pin
                if not piecePinned or pinDirection == (-1,self.enPassant[2]-c):
                    moves.append( Move( (r,c), (r-1,self.enPassant[2]), self.board, True) )    
            #######################################################################################             
                    
           
            if r-1 >= 0: # as long as we dont implement a pawn promotion solution, there can be a white pawn on the 8th rank which is r==0
                ############### regular forward pawn moves ##############
                if self.board[r-1][c] == "--": # check if the square above the pawn is clear, if so one square forward is a valid move
                    if not piecePinned or pinDirection == (-1,0):
                        moves.append( Move( (r,c), (r-1,c), self.board) ) 
                        if r==6 and self.board[r-2][c] == "--": # check now if also the second square above the pawn is clear, and if its the pawn's firs move i.e. its on row 6
                            moves.append( Move( (r,c), (r-2,c), self.board) ) 
                #################### Capturing ##########################
                if c-1 >= 0: # capture on the left. avoid accessing idxs off the board
                    if self.board[r-1][c-1][0] == 'b':
                        if not piecePinned or pinDirection == (-1,-1):
                            moves.append( Move( (r,c), (r-1,c-1), self.board) ) 
                if c+1 <= 7: # capture on the right. avoid accessing idxs off the board
                    if self.board[r-1][c+1][0] == 'b':
                        if not piecePinned or pinDirection == (-1,1):
                            moves.append( Move( (r,c), (r-1,c+1), self.board) )                   
        else: # black to move
            ###############################  black En-Passant  #########################################  
            # if enpassant is possible AND the color to move is white AND the pawn in question is on either side of the black pawn which just moved: 
            if self.enPassant[0] and self.enPassant[1] == 'b' and r==4 and ( c==(self.enPassant[2]+1) or c==(self.enPassant[2]-1) ):
                # print("print me") 
                # verify that the pawn is not pinned or that its en-passing in the direction of the pin
                if not piecePinned or pinDirection == (1,self.enPassant[2]-c):
                    moves.append( Move( (r,c), (r+1,self.enPassant[2]), self.board, True) )    
            #######################################################################################   
            if r+1 <= 7:
                ############### regular forward pawn moves ##############
                if self.board[r+1][c] == "--": # check if the square above the pawn is clear, if so one square forward is a valid move
                    if not piecePinned or pinDirection == (1,0):
                        moves.append( Move( (r,c), (r+1,c), self.board) ) 
                        if r==1 and self.board[r+2][c] == "--"  :
                            moves.append( Move( (r,c), (r+2,c), self.board) ) 
                #################### Capturing ##########################
                if c-1 >= 0: # avoid accessing idxs off the board
                    if self.board[r+1][c-1][0] == 'w':
                        if not piecePinned or pinDirection == (1,-1):
                            moves.append( Move( (r,c), (r+1,c-1), self.board) ) 
                if c+1 <= 7: # avoid accessing idxs off the board
                    if self.board[r+1][c+1][0] == 'w':
                        if not piecePinned or pinDirection == (1,1):
                            moves.append( Move( (r,c), (r+1,c+1), self.board) )         
    def getRookMoves(self, r,c, moves):     
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # itterate through the pinned pieces list and determine if the pawn 
                                                  # which we want to generate moves for, is a pinned piece or not.
                                                  # we itterate backwards to prevent possible bugs arrising from deleting an item from the list.
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != 'Q':  # lets say the queen is pinned by a bishop, thus removing it from thelist of pinned pieces now,
                                                # will make the quun able to move, when getQueenMoves() calls getBishopMoves()
                                                # this we dont want to remove it yet, we will however remove it in getBishopMoves()
                    self.pins.remove(self.pins[i])      #why the hell should i remove a pin from the list it just takes alot of time updating the list (done in the backround but still..)                          
                break
        directions = ( (-1,0), (1,0), (0,-1), (0,1) ) # up left down right
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]): # you cant negate a tuple like -d because its not a number, but the ellements inside the tuple are numbers which can be negated
                for i in range(1,8):
                    endRow = r + d[0]*i
                    endCol = c + d[1]*i
                    if 0<=endRow<=7 and 0<=endCol<=7: # the square isnt off the board                
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break # if there's an enemy piece in a square, the Rook cant go past it! we have to break the loop
                        elif endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        else: # there's no free square\enemy piece so there must be an ally piece which we cant go past in this direcion, so beak the inner loop! (the loop in the direction of the ally piece)
                            break
    def getBishopMoves(self, r,c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # itterate through the pinned pieces list and determine if the pawn 
                                                  # which we want to generate moves for, is a pinned piece or not.
                                                  # we itterate backwards to prevent possible bugs arrising from deleting an item from the list.
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i]) #why the hell should i remove a pin from the list it just takes alot of time updating the list (done in the backround but still..)
                break
        
        directions = ( (-1,-1), (-1,1), (1,-1), (1,1) ) # up left down right
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                for i in range(1,8):
                    endRow = r + d[0]*i
                    endCol = c + d[1]*i
                    if 0<=endRow<=7 and 0<=endCol<=7:
                        endPiece = self.board[endRow][endCol]                
                        if endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break # if there's an enemy piece in a square, the Rook cant go past it! we have to break the loop
                        elif endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        else: # there's no free square\enemy piece so there must be an ally piece which we cant go past in this direcion, so beak the inner loop! (the loop in the direction of the ally piece)
                            break
    def getKnightMoves(self, r,c, moves):
        for i in range(len(self.pins)-1, -1, -1): # itterate through the pinned pieces list and determine if the knight 
                                                  # which we want to generate moves for, is a pinned piece or not.
                                                  # we itterate backwards to prevent possible bugs arrising from deleting an item from the list.
            if self.pins[i][0] == r and self.pins[i][1] == c:
                self.pins.remove(self.pins[i]) #why the hell should i remove a pin from the list it just takes alot of time updating the list (done in the backround but still..)
                return moves # if the knight is pinned it cannot move towards the pin nor capure a pinning pieace,
                             # due to the nature of the knights movement
                             
        # the knight is not pinned so it may move:
        if self.WhiteToMove:
            # move up/down 2 squares and 1 square sideways
            if (r+2) <= 7: 
                if (c+1) <= 7:
                    if self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0] == 'b':
                        moves.append( Move( (r,c), (r+2,c+1), self.board) )
                if (c-1) >= 0:
                    if self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0] == 'b':
                        moves.append( Move( (r,c), (r+2,c-1), self.board) )
            if (r-2) >= 0:
                if (c+1) <= 7:
                    if self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0] == 'b':
                        moves.append( Move( (r,c), (r-2,c+1), self.board) )
                if (c-1) >= 0:
                    if self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0] == 'b':
                        moves.append( Move( (r,c), (r-2,c-1), self.board) )       
            # move sideways 2 squares and 1 square up/down
            if (c+2) <= 7:
                if (r+1) <= 7:
                    if self.board[r+1][c+2] == "--" or self.board[r+1][c+2][0] == 'b':
                        moves.append( Move( (r,c), (r+1,c+2), self.board) )
                if (r-1) >= 0:
                    if self.board[r-1][c+2] == "--" or self.board[r-1][c+2][0] == 'b':
                        moves.append( Move( (r,c), (r-1,c+2), self.board) )
            if (c-2) >= 0:
                if (r+1) <= 7:
                    if self.board[r+1][c-2] == "--" or self.board[r+1][c-2][0] == 'b':
                        moves.append( Move( (r,c), (r+1,c-2), self.board) )
                if (r-1) >= 0:
                    if self.board[r-1][c-2] == "--" or self.board[r-1][c-2][0] == 'b':
                        moves.append( Move( (r,c), (r-1,c-2), self.board) )          
        else:
            # move up/down 2 squares and 1 square sideways
            if (r+2) <= 7: 
                if (c+1) <= 7:
                    if self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0] == 'w':
                        moves.append( Move( (r,c), (r+2,c+1), self.board) )
                if (c-1) >= 0:
                    if self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0] == 'w':
                        moves.append( Move( (r,c), (r+2,c-1), self.board) )
            if (r-2) >= 0:
                if (c+1) <= 7:
                    if self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0] == 'w':
                        moves.append( Move( (r,c), (r-2,c+1), self.board) )
                if (c-1) >= 0:
                    if self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0] == 'w':
                        moves.append( Move( (r,c), (r-2,c-1), self.board) )       
            # move sideways 2 squares and 1 square up/down
            if (c+2) <= 7:
                if (r+1) <= 7:
                    if self.board[r+1][c+2] == "--" or self.board[r+1][c+2][0] == 'w':
                        moves.append( Move( (r,c), (r+1,c+2), self.board) )
                if (r-1) >= 0:
                    if self.board[r-1][c+2] == "--" or self.board[r-1][c+2][0] == 'w':
                        moves.append( Move( (r,c), (r-1,c+2), self.board) )
            if (c-2) >= 0:
                if (r+1) <= 7:
                    if self.board[r+1][c-2] == "--" or self.board[r+1][c-2][0] == 'w':
                        moves.append( Move( (r,c), (r+1,c-2), self.board) )
                if (r-1) >= 0:
                    if self.board[r-1][c-2] == "--" or self.board[r-1][c-2][0] == 'w':
                        moves.append( Move( (r,c), (r-1,c-2), self.board) )       
    def getQueenMoves(self, r,c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)          
    def getKingMoves(self, r,c, moves):
        kingMoves = ( (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1) )
        allyColor = "w" if self.WhiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0<=endRow<=7 and 0<=endCol<=7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == allyColor: # there is an ally piece there, thus the king cant move there
                    continue
                elif self.isKingInCheck(endRow,endCol,allyColor): # if the king will be in check in the (endRow,endCol) square, he cant move there
                    continue
                else:                          
                    moves.append(Move((r,c), (endRow,endCol), self.board))
        ###################### Check if castling is possible on eiher side  ###########             
        if self.canCastleKingSide(r,c,allyColor):
            # print(allyColor,"can castle kingside")
            moves.append( Move((r,c), (r,c+2), self.board,False, [True,True] ) )
        if self.canCastleQueenSide(r,c,allyColor):
            # print(allyColor,"can castle queenside")
            moves.append( Move((r,c), (r,c-2), self.board,False, [True,False] ) )  
            
    def isKingInCheck(self, kingRow, kingCol, allyColor):
    # =============================================================================
    # This function is a modified thinner version of checkForPinsAndChecks() that only returns
    # a boolean value if the piece at (kingRow,kingCol) is threatend (i.e. if the kings location is sent, that means check)
    # this function is only for generating the allowed king moves, and thats why ive created this thin version
    # of checkForPinsAndChecks() because pins still allow for king move thus the fat version just took unnecessary space
    # =============================================================================        
        enemyColor = 'b' if allyColor=='w' else 'w'
            
        # go in either one of the following directions (all orthogonal and diagonal possibilities around the king)
        # and check if there's an enemy piece that threatens our king at (startRow,startCol)
        directions = ( (-1,0), (0,-1), (1,0), (0,1),   # idxs 0 to 3 are orthogonal directions
                      (-1,-1), (-1,1), (1,-1), (1,1) ) # idxs 4 to 7 are  diagonal directions
        
        for j in range(len(directions)): # for each direction in "directions"
             d = directions[j]
             for i in range(1,8): # go through all the squares in each direction (as long as they are on the board of course 0<=endRow<=7 and 0<=endCol<=7 )
                 endRow = kingRow + d[0]*i
                 endCol = kingCol + d[1]*i
                 if 0<=endRow<=7 and 0<=endCol<=7:
                     endPiece = self.board[endRow][endCol] # get the piece on that square (may be an empty square "--")
                     if endPiece[0] == allyColor and endPiece[1] != 'K': # see explanations on why we must add : "and endPiece[1] != 'K'" as a condition, in (minute 36): https://www.youtube.com/watch?v=coAOXj6ZnSI&t=1908s&ab_channel=EddieSharick
                                                                         # to understand lets see an example: lets say the enemy queen is attacking the king from one square above the king. in that case this function checks if the king can move to all squares around its current location
                                                                         # however if we dont add the "and endPiece[1] != 'K'", the algorithm will think that the actual king is shielding the square below it! as the king is actually there as the function searches self.board.
                                                                         #  so we need to verify that the shielding piece (pinned ally piece) isnt the actual king for which we are checking valid moves 
                         break # it used to be continue, but no need to continue checking for checks in a direction shielded by an ally piece
                     elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # !.) note: (the dash '\' in the following if statement is the only way of dropping lines in python if statements https://stackoverflow.com/questions/53162/how-can-i-do-a-line-break-line-continuation-in-python)
                        if (0<=j<=3 and type == 'R') or \
                            (4<=j<=7 and type == 'B') or \
                            (i==1 and type == 'P' and ((enemyColor == 'w' and 6<=j<=7) or (enemyColor == 'b' and 4<=j<=5))) or\
                            (type == 'Q') or (i==1 and type =='K'): # unlike checkForPinsAndChecks() here weve got to check if the kings are close together which is illegal
                                # print(allyColor,"king is threatend on: r =",kingRow," c =",kingCol,"by enemy", type,"on",(endRow,endCol),". threat direction is",d, "and i =",i,"j =",j)
                                return True
                        else: # we've reached an enemy piece but its not a piece that threatens (kingRow,kingCol),
                              # e.g. an enemy pawn which is more than a square away from (kingRow,kingCol) in the j'th direction,
                              # thus, theres no need to check for any more pieces (except the enemy knight which is checked seperately) that 
                              # threat (kingRow,kingCol), so we break from the inner loop which itterates through squares in the j'th direction
                            break
                                
                 else:
                     break # endRow or endCol are the off board
        # check for knight checks. a night is an odd duck, so we verify its checks seperately
        knightMoves = ( (-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1) )                       
        for m in knightMoves:
            endRow = kingRow + m[0]
            endCol = kingCol + m[1]
            if 0<=endRow<=7 and 0<=endCol<=7:
                endPiece = self.board[endRow][endCol]   
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # enemy knight attecking te king
                    return True
        return False    
    def canCastleQueenSide(self,r,c,allyColor):
    # =============================================================================
    # this function return a boolean value True iff the allyColor can castle queenside, according to the following rules.
    # Castling is permissible provided all of the following conditions hold: (see wikipedia page on Castling)
    # 
    # (1) The castling must be kingside or queenside.
    # (2) Neither the king nor the chosen rook has previously moved.
    # (3) There are no pieces between the king and the chosen rook.
    # (4) The king is not currently in check.
    # (5) The king does not pass through a square that is attacked by an enemy piece.
    # (6) The king does not end up in check. 
    # =============================================================================
                    
        # check if the king in question has moved, if so castleing is prohibitted
        if self.WhiteToMove and self.whiteKingMoveCount != 0:
            return False
        elif not self.WhiteToMove and self.blackKingMoveCount != 0:
            return False
        
        # Check if the rook on the king side is even there
        if self.WhiteToMove and self.board[7][0] != "wR":
            return False
        elif not self.WhiteToMove and self.board[0][0] != "bR":
            return False       
        
        # check if the moving's color kingside rook has moved, if so castleing is prohibitted
        if self.WhiteToMove and self.whiteQueensideRookMoveCount !=0 :
            return False
        elif not self.WhiteToMove and self.blackQueensideRookMoveCount != 0:
            return False      
        # now go through the squares starting in the kings location up to the rook's location and veriy that the king is not currntly in check
        # nor that any of the squares inbetween the king and rook is threatend, aswell as vacant     
        for i in range(0,4):
           endRow = r 
           endCol = c - 1 * i
           if i != 0 and self.board[endRow][endCol] != "--":  # if the squares inbetween the king and rook arent vacant -> cant castle
               return False
           if i != 3 and self.isKingInCheck(endRow,endCol,allyColor):    # if the Squares hat the king is passing through are threatend (including current king check) -> cant castle
               return False
        return True
    def canCastleKingSide(self,r,c,allyColor):
    # =============================================================================
    # this function return a boolean value True iff the allyColor can castle kingside, according to the following rules.
    # Castling is permissible provided all of the following conditions hold: (see wikipedia page on Castling)
    # 
    # (1) The castling must be kingside or queenside.
    # (2) Neither the king nor the chosen rook has previously moved.
    # (3) There are no pieces between the king and the chosen rook.
    # (4) The king is not currently in check.
    # (5) The king does not pass through a square that is attacked by an enemy piece.
    # (6) The king does not end up in check. 
    # =============================================================================
                    
        # check if the king in question has moved, if so castling is prohibitted
        if self.WhiteToMove and self.whiteKingMoveCount != 0:
            return False
        elif not self.WhiteToMove and self.blackKingMoveCount != 0:
            return False
        
        # Check if the rook on the king side is even there
        if self.WhiteToMove and self.board[7][7] != "wR":
            return False
        elif not self.WhiteToMove and self.board[0][7] != "bR":
            return False       
        
        # check if the moving's color kingside rook has moved, if so castling is prohibitted
        if self.WhiteToMove and self.whiteKingsideRookMoveCount != 0 :
            return False
        elif not self.WhiteToMove and self.blackKingsideRookMoveCount != 0 :
            return False      
        # now go through the squares starting in the kings location up to the rook's location and veriy that the king is not currntly in check
        # nor that any of the squares inbetween the king and rook is threatend, aswell as vacant     
        for i in range(0,3):
           endRow = r 
           endCol = c + 1 * i
           if i != 0 and self.board[endRow][endCol] != "--":  # if the squares inbetween the king and rook arent vacant -> cant castle
               return False
           if self.isKingInCheck(endRow,endCol,allyColor):    # if the Squares hat the king is passing through are threatend (including current king check) -> cant castle
               return False
        return True
                
    
    
class Move():
    
    # lets creat a dictionary to convert from coordinates to chess notation and vise versa:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsoRanks = {v: k for k, v in ranksToRows.items()} # this is a cool python feature. we can define 
                                                        # this dict by using the last dict we created as an itterable:
                                                        # we just define each entry in the dict as "v": k
                                                        # where "k": v are the entries of the last dict we defined 
    filesTocCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k,v in filesTocCols.items()}
    
    
    
    def __init__(self, startSq, endSq, board, enPass = False, castle = [False,False]):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] # might be an empty square "--"
        self.pieceCaptured = board[self.endRow][self.endCol] # might be an empty square "--"
        self.moveID = self.startRow * 1000 + self.startCol*100 + self.endRow * 10 + self.endCol #encode each move to a specific scalar ID like a hash function
        self.enPassant = enPass
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True
        self.isCastle = castle[0]
        self.isKingSideCastle = castle[1]

        # print("move ID: ", self.moveID)
    
    # we now add\overwrite the opperator "==" to the class "Move" by simply returning a boolean value TRUE
    # if two Move objects have the same moveID integer, instead of comparing each entry of two classes
    # and returning TRUE iff all the entries are equal (which is how the default opperator works)
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
            
        
    def getChessNotation(self):
        # write a string in semi-chess notation convention (we need to improve it but the jist is all the same)
        # e.g. e3e4 is taking a piece from e3 to e4
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endRow)
    def getRankFile(self, c, r):
        return self.colsToFiles[c]+ self.rowsoRanks[r] # appending strings by + opperator
        
        