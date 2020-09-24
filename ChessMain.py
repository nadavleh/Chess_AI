import pygame as p
import ChessEngine # importing the ChessEngine file we are writing
import ChessAI 

WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #8x8 board
SQ_SIZE = HEIGHT // DIMENSION #this is the size of each square
MAX_FPS = 15 #for animations later on
IMAGES = {}

# =============================================================================
# initialize a global dictionary of images
# this will be called once in the main
# =============================================================================

def loadImages():
    pieces = ["wP","wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale( p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    # we can now access images by e.g. IMAGES['wP']


# =============================================================================
# the main drive for the code will handle user input and graphics updating
# =============================================================================
def main():
    p.init()  # try init above if poblems arrise due to dependencies
    screen  = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white")) # make the game window white initially (not neccessary)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # this is a flag variable for when a move is made
    moveCount = 0

    loadImages() # only do this once before the while loop, load the pieces images
    running = True
    sqSelected = ()   # no square is selected, keep track of the last click of the user ( a tuple in the form (row, col))
    playerClicks = [] # keep track of player clicks (in the form of two tuples [(6,4), (4,4) ]
                      #  where the first tuple is the click where we chose a piece and the second
                      # tuple is its designated aquare we chose)
                      
    gameOver = False
    ai = ChessAI.ChessAI()
    
    while running:
        # the method pygame.event records events from the opperating system,
        # which are related to the game window. events are essentialy muse clicks
        # or keyboard clicks. for example if the event type is "QUIT" it means
        # the user pressed the red x exit button. we essentialy pop the last event
        # recorded, query its type and act accordingly
        for e in p.event.get():
            # user pressed exit
            if e.type == p.QUIT:
                running = False
                p.quit()

            # mouse press handlers
            elif e.type == p.MOUSEBUTTONDOWN and gs.WhiteToMove: #########ADDED here: and gs.WhiteToMove: 
                location = p.mouse.get_pos() # pixel (x,y) location of the mouse

                col = location[0]//SQ_SIZE   # convert pixel coordinates to square coordinates
                row = location[1]//SQ_SIZE   # using "floor devision" opperator '//' see www.w3schools.com/python/python_operators.asp

                if sqSelected == (row, col): # the user already clicked this square in the
                                             # last loop run, i.e. the user selected the same square twice
                                             # which we want to make a "undo select"
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # so if the square selected is different from the last square selected,
                                                    # we append it to the list. now we need to make sure the list have just two moves
                                                    # and stop there.
                    if len(playerClicks) == 2:
                        # we can move the pices now, but to do that it would be a good practice
                        # to implement the movements via a designated class, which we add in the ChessEngine.py file.
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board) # create a "Move" object
                        # print(move.getChessNotation()) # print the move to the screen for debugging purpossess

                        # now, once the player have chosen a piece and a destination square we want to check if its a valid move
                        # inorder to do so we check if the move made by the plaer is in the validMoves array of "Move" objects.
                        # this python property is very nice and saves us lines of code by typing the "in" command, however python implements it
                        # by regular loops and compare each var in the "move" object to each of validMoves objects. we can speed this
                        # up by modifying the "==" opperator of the "Move" Class in such a way so that cheking if two "Move" objects are the same
                        # only by comparing an ID which is distinct for each move

                        for i in range(len(validMoves)): 
                        # =============================================================================
                        # we do it like this and not the shorter "if move in validMoves:"
                        # because that way we can make the move validMoves[i] which may
                        # have more information that the players move which has only initial
                        # square and end square, where the interlal move for instance may
                        # have information regarding en-passant or castling for example,
                        # which the player move doesnt have. However each move has its own ID number 
                        # based on the iniial and end squares, so if the player has entered a move with the same
                        # ID as a special move (e.g. a castling move), the move that will be made is the one 
                        # in the validMoves list (which has all the internal info needed), and not the players move.
                        # inorder to check if two move objects are equal, we have changed the "==" opperator
                        # of the Move class, so that two objects are equal iff two of them have the same ID    
                        # =============================================================================
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True # indicate that a move was made so we can update the valid moves
                                moveCount += 1

                                str = " white to move" if gs.WhiteToMove else " black to move"
                                print("moves made: ", moveCount, str)

                                sqSelected = () # reset user clicks. doesnt matter if a move was made or not
                                playerClicks = []
                            if not moveMade:  # if the user chooses a pawn by mistake and wants o choose another pawn, the computer would
                                              # think the player wanted to move one pawn over the other which is not a valid move, and thus will reset
                                              # the playerClicks list. so this "else" statement allows the player to choose the other pawn withot all the fuss as before
                                playerClicks = [sqSelected]

            elif not gameOver and not gs.WhiteToMove:           #########ADDED here: all of the elif
                score, move = ai.alphaBeta(gs, depth = 4)
                gs.makeMove(move)
                moveMade = True
                moveCount += 1


            # keyboard press handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo move by pressing 'z'
                    gs.undoMove()
                    # once the "to be deleted" move was made, the validMoves array
                    # was updated according to the new board position which we want to undo.
                    # Hence, we need to once more update the validMoves array according to te last position
                    moveMade = True
                elif e.key == p.K_i: #information
                    print("The valid moves are: ")
                    for move in validMoves:
                        print(move.pieceMoved[1], "to r =", move.endRow, " c =",move.endCol)

        # we only want to search for valid moves if a move was made, otherwise each
        # while loop itteration we will update the validMoves array, which is a
        # costly opperation, and will generate the same valid moves if a move
        # wasnt made.
        if moveMade:
            # print(gs.board)
            validMoves = gs.getValidMoves()
            # print("number of valid moves: ", len(validMoves) )
            moveMade = False

        ############### now if the game ended draw the result on the screen ############
        if gs.checkmate:
            # print("kaki kaki kaki")
            # gameOver = True
            if gs.WhiteToMove:
                # drawText(screen, 'Black Wins by Checkmate') # drawText() isnt working a the moment
                pass
            else:
                # drawText(screen, 'White Wins by Checkmate')  # drawText() isnt working a the moment
                pass
        elif gs.stalemate:
            # gameOver = True
            # drawText(screen, 'Stalemate')  # drawText() isnt working a the moment
            pass

        # now generate the chess board gaphics
        drawGameState(screen, gs, validMoves, sqSelected)       
        clock.tick(MAX_FPS)
        p.display.flip() # redraws the displayed frame, according to the MAX_FPS rate
        

def drawText(screen, text):
    font = p.font.get_default_font()#.SysFont('agencyfb', 25)
    textObject = font.render(text, True, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != (): #hughlight as long as the player actually choose a piece
        r,c = sqSelected # remember sqSelected is a tuple. this python syntax allows to assign the tuple vars into individual vars
        if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'): # this is a cool python feature that allows us to write the following 
                                                                  # line instead of the two lines. notice that the parenthesis is evaluated first,
                                                                  # and only then the "==" opperator. here we make sure that the square selected is actually a piece that can move
            s = p.Surface((SQ_SIZE,SQ_SIZE)) # we define a new surface object which will be the size of a board square. this surface
                                             # will be laid upon the screen i locations we will soon indicate. for now we choos its color and transperancy
            
            s.set_alpha(100) # transperency value -> 0 transperent; 255 solid\opaque
            s.fill(p.Color('blue')) # fill this surface with blue color whih has set_alpha(X) transperency
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE)) # blitting (drawing upon the screen) the Surface object s at location (c*SQ_SIZE,r*SQ_SIZE) which is the top right corner of the Square selected
                                                 # NOTICE: the blit() method asks for (x,y) locations on the screen that corresponds to tuples of the form (c,r) and not (r,c) as we are used to (which are wssentialy (y,x) board coordinates)  
            #highlight moves from the square selected (available move locations)
            s.fill(p.Color('yellow')) # now set the highlight color to yellow and blit it upon the possible end squares of the chosen piece
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
def highlightLastMove(screen, gs):
    if len(gs.MoveLog) != 0:
        lastMove = gs.MoveLog[-1]
        startTuple = (lastMove.startRow,lastMove.startCol)
        endTuple = (lastMove.endRow,lastMove.endCol)
        s = p.Surface((SQ_SIZE,SQ_SIZE))
        s.set_alpha(30)
        s.fill(p.Color('green'))
        screen.blit(s,(startTuple[1]*SQ_SIZE,startTuple[0]*SQ_SIZE))
        screen.blit(s,(endTuple[1]*SQ_SIZE,endTuple[0]*SQ_SIZE))
# =============================================================================
# the following functions are responsible for all graphics within a current game
# state
# =============================================================================
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected) #highlight in blue the square on which a piece which is selected is on, and its possible moves in yellow
    drawPieces(screen, gs.board) # draw the pieces upon the squares
    highlightLastMove(screen, gs)
def drawBoard(screen):
    # notice that in a chess board, from whites perspective,
    # the white squares always appear when the sum of the square coordinates
    # are even. respectivly, the black square's coordinates sum is always odd.
    # By setting the color vector to have white at index 0 and black at index 1
    # we can easily create the graphical board with two loops and modulo 2 to
    # access the desired color
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece],  p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE) )

if __name__ == "__main__":
    main()
