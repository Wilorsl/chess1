import pygame as pg
from pygame import *
import math

# Setting the window size for the chessboard
size = 700
WIN = display.set_mode((size, size))
display.set_caption('Chess')
clock = time.Clock()
font.init()

# Defining the size of a single cell on the chessboard
scale = size / 8

# Creating a list of rectangles to represent the chessboard cells
RectList = []
for i in range(8):  # rows
    for j in range(4):  # columns
        RectList.append(
            pg.Rect(((i % 2) * scale + 2 * j * scale, i * scale, scale, scale)))

# Initial setup of the chessboard with pieces represented by strings
Board = [
    ['R1', 'N1', 'B1', 'Q1', 'K1', 'B1', 'N1', 'R1'],  # Black
    ['p1', 'p1', 'p1', 'p1', 'p1', 'p1', 'p1', 'p1'],  # pieces
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0'],  # White
    ['R0', 'N0', 'B0', 'Q0', 'K0', 'B0', 'N0', 'R0']   # pieces
]

# Dictionary defining attack patterns for each piece type
AttackDict = {
    'R': [[0, 1], [1, 0], [0, -1], [-1, 0], 1],  # Rook
    'B': [[1, 1], [-1, -1], [1, -1], [-1, 1], 1],  # Bishop
    # Queen
    'Q': [[1, 1], [-1, -1], [1, -1], [-1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], 1],
    # Knight
    'N': [[1, 2], [2, 1], [-1, -2], [-2, -1], [-1, 2], [-2, 1], [1, -2], [2, -1], 0],
    'P': [[-1, -1], [1, -1], 0],  # White pawn
    'p': [[-1, 1], [1, 1], 0],  # Black pawn
    'K': [[1, 1], [-1, -1], [1, -1], [-1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], 0]  # King
}


# Function to draw the chessboard background
def DrawBg():
    pg.draw.rect(WIN, (181, 136, 99), (0, 0, size, size))
    for R in RectList:
        pg.draw.rect(WIN, ((240, 217, 181)), R)


# Function to draw the chess pieces on the board
def DrawPieces():
    piece_scale = size / 9  # Scale for resizing piece images
    y = 0  # Row
    for Brd in Board:
        x = 0  # Column
        for B in Brd:
            if Board[y][x] != '.':  # If the cell is not empty
                # Load and draw the piece image at the correct position
                WIN.blit(transform.scale(pg.image.load(
                    Board[y][x] + '.png'), (piece_scale, piece_scale)), (x / 2 + x * scale, y / 2 + y * scale))
            x += 1
        y += 1


# Function to check if the king is in check
def CheckCheck(B_W):  # B_W is 0 for white king, 1 for black king
    y = 0  # Row
    for Brd in Board:
        x = 0  # Column
        for B in Brd:
            if B != '.':  # If the cell is not empty
                if B[1] != B_W:  # If the piece belongs to the opponent
                    # Loop through attack patterns
                    for shift in AttackDict[B[0]][0:-1]:
                        pos = [x, y]  # Starting position
                        # Move in the attack direction
                        for i in range(AttackDict[B[0]][-1] * 6 + 1):
                            pos[0] += shift[0]
                            pos[1] += shift[1]
                            # Stop if the position is out of bounds
                            if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                                break
                            # Stop if the path is blocked by another piece
                            if Board[pos[1]][pos[0]] != '.':
                                if Board[pos[1]][pos[0]] != 'K' + B_W:  # If it's not the king
                                    break
                                # If it's the king, return True (king is in check)
                                else:
                                    return True
            x += 1
        y += 1
    return False  # Return False if the king is not in check


# Function to show possible moves for a piece
def ShowVariants(x, y):
    global Variants  # List of possible moves
    Variants = []
    B = Board[y][x]  # Get the piece at the given position
    for shift in AttackDict[B[0]][0:-1]:  # Loop through attack patterns
        pos = [x, y]  # Starting position
        # Move in the attack direction
        for i in range(AttackDict[B[0]][-1] * 6 + 1):
            pos[0] += shift[0]
            pos[1] += shift[1]
            # Stop if the position is out of bounds
            if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                break
            # Stop if the path is blocked by another piece
            if Board[pos[1]][pos[0]] != '.':
                if Board[pos[1]][pos[0]][1] != Board[y][x][1]:  # If it's an opponent's piece
                    # Add the position to the list
                    Variants.append([pos[0], pos[1]])
                    break
                else:  # If it's a friendly piece, stop
                    break
            elif B[0] != 'p' and B[0] != 'P':  # If it's not a pawn
                # Add the position to the list
                Variants.append([pos[0], pos[1]])

    # Handle pawn-specific moves
    if B[0] == 'P':  # If it's a white pawn
        pos = [x, y]
        for i in range((y == 6) + 1):  # Allow two steps if the pawn is in its starting position
            pos[1] -= 1  # Move up
            if pos[1] < 0:  # Stop if the position is out of bounds
                break
            if Board[pos[1]][pos[0]] != '.':  # Stop if the path is blocked
                break
            Variants.append([pos[0], pos[1]])  # Add the position to the list

    if B[0] == 'p':  # If it's a black pawn
        pos = [x, y]
        for i in range((y == 1) + 1):  # Allow two steps if the pawn is in its starting position
            pos[1] += 1  # Move down
            if pos[1] > 7:  # Stop if the position is out of bounds
                break
            if Board[pos[1]][pos[0]] != '.':  # Stop if the path is blocked
                break
            Variants.append([pos[0], pos[1]])  # Add the position to the list

    # Remove moves that put the king in check
    ForDeletion = []  # List of moves to remove
    Board[y][x] = '.'  # Temporarily remove the piece from the board
    for V in Variants:  # Loop through possible moves
        # Remember the piece at the target position
        remember = Board[V[1]][V[0]]
        Board[V[1]][V[0]] = B  # Move the piece to the target position
        if CheckCheck(B[1]):  # Check if the king is in check
            # Add the move to the list of moves to remove
            ForDeletion.append(V)
        # Restore the piece at the target position
        Board[V[1]][V[0]] = remember
    Board[y][x] = B  # Restore the piece at its original position
    for Del in ForDeletion:  # Loop through moves to remove
        Variants.remove(Del)  # Remove the move from the list

    # Handle castling for kings
    if Board[y][x] == 'K0':  # If it's the white king
        global castlingL0, castlingR0  # Castling flags for white
        # Check if castling is possible on the left
        if Board[7][0:5] == ['R0', '.', '.', '.', 'K0'] and castlingL0:
            Board[7][2], Board[7][3] = 'K0', 'K0'  # Temporarily move the king
            if CheckCheck('0') == 0:  # Check if the king is not in check
                Variants.append([2, 7])  # Add the castling move to the list
            Board[7][2], Board[7][3] = '.', '.'  # Restore the board
        # Check if castling is possible on the right
        if Board[7][4:8] == ['K0', '.', '.', 'R0'] and castlingR0:
            Board[7][5], Board[7][6] = 'K0', 'K0'  # Temporarily move the king
            if CheckCheck('0') == 0:  # Check if the king is not in check
                Variants.append([6, 7])  # Add the castling move to the list
            Board[7][5], Board[7][6] = '.', '.'  # Restore the board
    if Board[y][x] == 'K1':  # If it's the black king
        global castlingL1, castlingR1  # Castling flags for black
        # Check if castling is possible on the left
        if Board[0][0:5] == ['R1', '.', '.', '.', 'K1'] and castlingL1:
            Board[0][2], Board[0][3] = 'K1', 'K1'  # Temporarily move the king
            if CheckCheck('1') == 0:  # Check if the king is not in check
                Variants.append([2, 0])  # Add the castling move to the list
            Board[0][2], Board[0][3] = '.', '.'  # Restore the board
        # Check if castling is possible on the right
        if Board[0][4:8] == ['K1', '.', '.', 'R1'] and castlingR1:
            Board[0][5], Board[0][6] = 'K1', 'K1'  # Temporarily move the king
            if CheckCheck('1') == 0:  # Check if the king is not in check
                Variants.append([6, 0])  # Add the castling move to the list
            Board[0][5], Board[0][6] = '.', '.'  # Restore the board


# Function to check for checkmate or stalemate
def CheckCheckMate(B_W):
    global Variants  # List of possible moves
    y = 0  # Row
    for Brd in Board:
        x = 0  # Column
        for B in Brd:
            if B[-1] == B_W:  # If the piece belongs to the current player
                ShowVariants(x, y)  # Show possible moves for the piece
                if len(Variants) > 0:  # If there are valid moves
                    Variants = []  # Reset the list of moves
                    return 0  # Return 0 (no checkmate or stalemate)
            x += 1
        y += 1
    if CheckCheck(B_W):  # If the king is in check
        Variants = []  # Reset the list of moves
        return 1  # Return 1 (checkmate)
    else:  # If the king is not in check
        Variants = []  # Reset the list of moves
        return 2  # Return 2 (stalemate)


Variants = []  # List of possible moves
DrawBg()
DrawPieces()
Turn = 0  # Initialize the turn (0 for black, 1 for white)
game = 1  # Game state (1 for running, 0 for stopped)
check = 0  # Game state check (0 for normal, 1 for checkmate, 2 for stalemate)
# Castling flags for white (left and right)
castlingL0, castlingR0 = True, True
# Castling flags for black (left and right)
castlingL1, castlingR1 = True, True

while game:  # Main game loop
    # Handle pawn promotion for white
    if Board[0].count('P0') and Turn == 1:  # If a white pawn reaches the last row
        Turn = -1  # Temporarily disable normal moves
        PawnX = Board[0].index('P0')  # Get the column of the pawn
        # Display promotion options (queen, rook, bishop, knight)
        WIN.blit(transform.scale(image.load(
            'Q0.png'), (40, 40)), (PawnX * 80, 0))  # TO RESIZE
        WIN.blit(transform.scale(image.load('R0.png'),  # TO RESIZE
                 (40, 40)), (40 + PawnX * 80, 0))  # TO RESIZE
        WIN.blit(transform.scale(image.load(  # TO RESIZE
            'B0.png'), (40, 40)), (PawnX * 80, 40))  # TO RESIZE
        WIN.blit(transform.scale(image.load('H0.png'),  # TO RESIZE
                 (40, 40)), (40 + PawnX * 80, 40))  # TO RESIZE

    # Handle pawn promotion for black
    if Board[7].count('p1') and Turn == 0:  # If a black pawn reaches the last row
        Turn = -2  # Temporarily disable normal moves
        PawnX = Board[7].index('p1')  # Get the column of the pawn
        # Display promotion options (queen, rook, bishop, knight)
        WIN.blit(transform.scale(image.load(
            'Q1.png'), (40, 40)), (PawnX * 80, 560))  # TO RESIZE
        WIN.blit(transform.scale(image.load('R1.png'),  # TO RESIZE
                 (40, 40)), (40 + PawnX * 80, 560))  # TO RESIZE
        WIN.blit(transform.scale(image.load(  # TO RESIZE
            'B1.png'), (40, 40)), (PawnX * 80, 600))  # TO RESIZE
        WIN.blit(transform.scale(image.load('H1.png'),  # TO RESIZE
                 (40, 40)), (40 + PawnX * 80, 600))  # TO RESIZE

    for e in event.get():
        if e.type == QUIT:
            game = 0  # Stop the game

        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:  # Left mouse button pressed
            if Turn == -1:  # Handle white pawn promotion
                x, y = (e.pos)  # Get the mouse position
                if PawnX + 1 > x / 80 >= PawnX and y < 80:  # Check if the click is within the promotion area
                    x = x % 80  # Get the relative x-coordinate
                    if 40 > x >= 0 and 40 > y >= 0:  # Promote to queen
                        Board[0][PawnX] = 'Q0'
                    elif 40 > x >= 0 and 80 > y >= 40:  # Promote to bishop
                        Board[0][PawnX] = 'B0'
                    elif 80 > x >= 40 and 40 > y >= 0:  # Promote to rook
                        Board[0][PawnX] = 'R0'
                    elif 80 > x >= 40 and 80 > y >= 40:  # Promote to knight
                        Board[0][PawnX] = 'H0'
                    Turn = 1  # Switch back to white's turn
                    DrawBg()
                    DrawPieces()
                    check = CheckCheckMate('1')  # Check the game state
                    if check == 1:  # If white wins
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'WHITE WON', False, (30, 30, 30)), (260, 310))
                    if check == 2:  # If it's a draw
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'DRAW', False, (30, 30, 30)), (290, 310))
            if Turn == -2:  # Handle black pawn promotion
                x, y = (e.pos)  # Get the mouse position
                if PawnX + 1 > x / 80 >= PawnX and y >= 560:  # Check if the click is within the promotion area
                    x = x % 80  # Get the relative x-coordinate
                    if 40 > x >= 0 and 600 > y >= 560:  # Promote to queen
                        Board[7][PawnX] = 'Q1'
                    elif 40 > x >= 0 and 640 > y >= 600:  # Promote to bishop
                        Board[7][PawnX] = 'B1'
                    elif 80 > x >= 40 and 600 > y >= 560:  # Promote to rook
                        Board[7][PawnX] = 'R1'
                    elif 80 > x >= 40 and 640 > y >= 600:  # Promote to knight
                        Board[7][PawnX] = 'H1'
                    Turn = 0  # Switch back to black's turn
                    DrawBg()
                    DrawPieces()
                    check = CheckCheckMate('0')  # Check the game state
                    if check == 1:  # If black wins
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'BLACK WON', False, (30, 30, 30)), (260, 310))
                    if check == 2:  # If it's a draw
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'DRAW', False, (30, 30, 30)), (290, 310))

            else:  # Handle normal moves
                x, y = (e.pos)  # Get the mouse position
                # Convert to board coordinates
                x, y = math.floor(x / scale), math.floor(y / scale)
                if Board[y][x] != '.':  # If the clicked cell is not empty
                    # If the piece belongs to the current player
                    if Board[y][x][1] == str(Turn):
                        ShowVariants(x, y)  # Show possible moves for the piece
                        remember = [x, y]  # Remember the selected piece
                        for V in Variants:  # Highlight possible moves
                            pg.draw.circle(WIN, (200, 200, 200),
                                           (V[0] * scale + scale / 2, V[1] * scale + scale / 2), 10)
        if e.type == pg.MOUSEBUTTONUP and e.button == 1 and Turn != -1 and Turn != -2:  # Left mouse button released
            x, y = (e.pos)  # Get the mouse position
            # Convert to board coordinates
            x, y = math.floor(x / scale), math.floor(y / scale)
            if Variants.count([x, y]):  # If the move is valid
                Board[y][x] = Board[remember[1]][remember[0]]  # Move the piece
                # Clear the original position
                Board[remember[1]][remember[0]] = '.'

                # Handle castling for white
                if remember == [4, 7] and Board[y][x] == 'K0':
                    if [x, y] == [2, 7]:  # Left castling
                        Board[7][0] = '.'
                        Board[7][3] = 'R0'
                    if [x, y] == [6, 7]:  # Right castling
                        Board[7][7] = '.'
                        Board[7][5] = 'R0'
                # Handle castling for black
                if remember == [4, 0] and Board[y][x] == 'K1':
                    if [x, y] == [2, 0]:  # Left castling
                        Board[0][0] = '.'
                        Board[0][3] = 'R1'
                    if [x, y] == [6, 0]:  # Right castling
                        Board[0][7] = '.'
                        Board[0][5] = 'R1'

                # Update castling flags for white
                if Board[7][0] != 'R0':
                    castlingL0 = False
                if Board[7][7] != 'R0':
                    castlingR0 = False
                if Board[7][4] != 'K0':
                    castlingL0 = False
                    castlingR0 = False
                # Update castling flags for black
                if Board[0][0] != 'R1':
                    castlingL1 = False
                if Board[0][7] != 'R1':
                    castlingR1 = False
                if Board[0][4] != 'K1':
                    castlingL1 = False
                    castlingR1 = False

                Turn = 1 - Turn  # Switch the turn
                check = CheckCheckMate(str(Turn))  # Check the game state
                if check == 1:  # If it's checkmate
                    DrawBg()  # Redraw the chessboard background
                    DrawPieces()  # Redraw the chess pieces
                    if Turn == 0:  # If black wins
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'BLACK WON', False, (30, 30, 30)), (260, 310))
                    if Turn == 1:  # If white wins
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'WHITE WON', False, (30, 30, 30)), (260, 310))
                if check == 2:  # If it's a draw
                    WIN.blit(pg.font.SysFont(None, 30).render(
                        'DRAW', False, (30, 30, 30)), (290, 310))
                Variants = []
            if check == 0:  # If the game continues
                DrawBg()
                DrawPieces()
            Variants = []  # Reset the list of moves
    display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS
