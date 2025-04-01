import pygame as pg
from pygame import *
import math

# Window size
size = 700
WIN = display.set_mode((size, size))
display.set_caption('Chess')
clock = time.Clock()
font.init()

# Size of a single cell
scale = size / 8

# Create a list of rectangles for the chessboard
RectList = []
for i in range(8):
    for j in range(4):
        RectList.append(
            pg.Rect(((i % 2) * scale + 2 * j * scale, i * scale, scale, scale)))

# Initial chessboard setup
Board = [
    ['R1', 'N1', 'B1', 'Q1', 'K1', 'B1', 'N1', 'R1'],
    ['p1', 'p1', 'p1', 'p1', 'p1', 'p1', 'p1', 'p1'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0'],
    ['R0', 'N0', 'B0', 'Q0', 'K0', 'B0', 'N0', 'R0']
]

# Attack patterns for each piece
AttackDict = {
    'R': [[0, 1], [1, 0], [0, -1], [-1, 0], 1],  # Rook
    'B': [[1, 1], [-1, -1], [1, -1], [-1, 1], 1],  # Bishop
    # Queen
    'Q': [[1, 1], [-1, -1], [1, -1], [-1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], 1],
    # Knight
    'N': [[1, 2], [2, 1], [-1, -2], [-2, -1], [-1, 2], [-2, 1], [1, -2], [2, -1], 0],
    'P': [[-1, -1], [1, -1], 0],  # White Pawn
    'p': [[-1, 1], [1, 1], 0],  # Black Pawn
    'K': [[1, 1], [-1, -1], [1, -1], [-1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], 0]  # King
}

# Draw the chessboard background


def DrawBg():
    pg.draw.rect(WIN, (181, 136, 99), (0, 0, size, size))
    for R in RectList:
        pg.draw.rect(WIN, ((240, 217, 181)), R)

# Draw the chess pieces on the board


def DrawPieces():
    piece_scale = size / 9
    y = 0
    for Brd in Board:
        x = 0
        for B in Brd:
            if Board[y][x] != '.':
                WIN.blit(transform.scale(pg.image.load(
                    Board[y][x] + '.png'), (piece_scale, piece_scale)), (x / 2 + x * scale, y / 2 + y * scale))
            x += 1
        y += 1

# Check if the king is in check


def CheckShah(B_W):  # B_W is 0 for white king, 1 for black king
    y = 0
    for Brd in Board:
        x = 0
        for B in Brd:
            if B != '.':
                if B[1] != B_W:  # Opponent's piece
                    for shift in AttackDict[B[0]][0:-1]:
                        pos = [x, y]
                        for i in range(AttackDict[B[0]][-1] * 6 + 1):
                            pos[0] += shift[0]
                            pos[1] += shift[1]
                            if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                                break
                            if Board[pos[1]][pos[0]] != '.':
                                if Board[pos[1]][pos[0]] != 'K' + B_W:
                                    break
                                else:
                                    return True
            x += 1
        y += 1
    return False

# Show possible moves for a piece


def ShowVariants(x, y):
    global Variants
    Variants = []
    B = Board[y][x]
    for shift in AttackDict[B[0]][0:-1]:
        pos = [x, y]
        for i in range(AttackDict[B[0]][-1] * 6 + 1):
            pos[0] += shift[0]
            pos[1] += shift[1]
            if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                break
            if Board[pos[1]][pos[0]] != '.':
                if Board[pos[1]][pos[0]][1] != Board[y][x][1]:
                    Variants.append([pos[0], pos[1]])
                    break
                else:
                    break
            elif B[0] != 'p' and B[0] != 'P':
                Variants.append([pos[0], pos[1]])

    # Handle pawn-specific moves
    if B[0] == 'P':
        pos = [x, y]
        for i in range((y == 6) + 1):
            pos[1] -= 1
            if pos[1] < 0:
                break
            if Board[pos[1]][pos[0]] != '.':
                break
            Variants.append([pos[0], pos[1]])

    if B[0] == 'p':
        pos = [x, y]
        for i in range((y == 1) + 1):
            pos[1] += 1
            if pos[1] > 7:
                break
            if Board[pos[1]][pos[0]] != '.':
                break
            Variants.append([pos[0], pos[1]])

    # Remove moves that put the king in check
    ForDeletion = []
    Board[y][x] = '.'
    for V in Variants:
        remember = Board[V[1]][V[0]]
        Board[V[1]][V[0]] = B
        if CheckShah(B[1]):
            ForDeletion.append(V)
        Board[V[1]][V[0]] = remember
    Board[y][x] = B
    for Del in ForDeletion:
        Variants.remove(Del)

    # Handle castling for kings
    if Board[y][x] == 'K0':
        global castlingL0, castlingR0
        if Board[7][0:5] == ['R0', '.', '.', '.', 'K0'] and castlingL0:
            Board[7][2], Board[7][3] = 'K0', 'K0'
            if CheckShah('0') == 0:
                Variants.append([2, 7])
            Board[7][2], Board[7][3] = '.', '.'
        if Board[7][4:8] == ['K0', '.', '.', 'R0'] and castlingR0:
            Board[7][5], Board[7][6] = 'K0', 'K0'
            if CheckShah('0') == 0:
                Variants.append([6, 7])
            Board[7][5], Board[7][6] = '.', '.'
    if Board[y][x] == 'K1':
        global castlingL1, castlingR1
        if Board[0][0:5] == ['R1', '.', '.', '.', 'K1'] and castlingL1:
            Board[0][2], Board[0][3] = 'K1', 'K1'
            if CheckShah('1') == 0:
                Variants.append([2, 0])
            Board[0][2], Board[0][3] = '.', '.'
        if Board[0][4:8] == ['K1', '.', '.', 'R1'] and castlingR1:
            Board[0][5], Board[0][6] = 'K1', 'K1'
            if CheckShah('1') == 0:
                Variants.append([6, 0])
            Board[0][5], Board[0][6] = '.', '.'

# Check for checkmate or stalemate


def CheckCheckMate(B_W):
    global Variants
    y = 0
    for Brd in Board:
        x = 0
        for B in Brd:
            if B[-1] == B_W:
                ShowVariants(x, y)
                if len(Variants) > 0:
                    Variants = []
                    return 0
            x += 1
        y += 1
    if CheckShah(B_W):
        Variants = []
        return 1  # Checkmate
    else:
        Variants = []
        return 2  # Stalemate


# Main game loop
Variants = []
DrawBg()
DrawPieces()
Turn = 0
game = 1
check = 0
castlingL0, castlingR0 = True, True
castlingL1, castlingR1 = True, True

while game:
    # Handle pawn promotion for white
    if Board[0].count('P0') and Turn == 1:
        Turn = -1
        PawnX = Board[0].index('P0')
        WIN.blit(transform.scale(image.load(
            'Q0.png'), (40, 40)), (PawnX * 80, 0))
        WIN.blit(transform.scale(image.load('R0.png'),
                 (40, 40)), (40 + PawnX * 80, 0))
        WIN.blit(transform.scale(image.load(
            'B0.png'), (40, 40)), (PawnX * 80, 40))
        WIN.blit(transform.scale(image.load('H0.png'),
                 (40, 40)), (40 + PawnX * 80, 40))

    # Handle pawn promotion for black
    if Board[7].count('p1') and Turn == 0:
        Turn = -2
        PawnX = Board[7].index('p1')
        WIN.blit(transform.scale(image.load(
            'Q1.png'), (40, 40)), (PawnX * 80, 560))
        WIN.blit(transform.scale(image.load('R1.png'),
                 (40, 40)), (40 + PawnX * 80, 560))
        WIN.blit(transform.scale(image.load(
            'B1.png'), (40, 40)), (PawnX * 80, 600))
        WIN.blit(transform.scale(image.load('H1.png'),
                 (40, 40)), (40 + PawnX * 80, 600))

    for e in event.get():
        if e.type == QUIT:
            game = 0

        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:  # Left mouse button pressed
            if Turn == -1:
                x, y = (e.pos)
                if PawnX + 1 > x / 80 >= PawnX and y < 80:
                    x = x % 80
                    if 40 > x >= 0 and 40 > y >= 0:
                        Board[0][PawnX] = 'Q0'
                    elif 40 > x >= 0 and 80 > y >= 40:
                        Board[0][PawnX] = 'B0'
                    elif 80 > x >= 40 and 40 > y >= 0:
                        Board[0][PawnX] = 'R0'
                    elif 80 > x >= 40 and 80 > y >= 40:
                        Board[0][PawnX] = 'H0'
                    Turn = 1
                    DrawBg()
                    DrawPieces()
                    check = CheckCheckMate('1')
                    if check == 1:
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'WHITE WON', False, (30, 30, 30)), (260, 310))
                    if check == 2:
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'DRAW', False, (30, 30, 30)), (290, 310))
            if Turn == -2:
                x, y = (e.pos)
                if PawnX + 1 > x / 80 >= PawnX and y >= 560:
                    x = x % 80
                    if 40 > x >= 0 and 600 > y >= 560:
                        Board[7][PawnX] = 'Q1'
                    elif 40 > x >= 0 and 640 > y >= 600:
                        Board[7][PawnX] = 'B1'
                    elif 80 > x >= 40 and 600 > y >= 560:
                        Board[7][PawnX] = 'R1'
                    elif 80 > x >= 40 and 640 > y >= 600:
                        Board[7][PawnX] = 'H1'
                    Turn = 0
                    DrawBg()
                    DrawPieces()
                    check = CheckCheckMate('0')
                    if check == 1:
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'BLACK WON', False, (30, 30, 30)), (260, 310))
                    if check == 2:
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'DRAW', False, (30, 30, 30)), (290, 310))

            else:
                x, y = (e.pos)
                x, y = math.floor(x / scale), math.floor(y / scale)
                if Board[y][x] != '.':
                    if Board[y][x][1] == str(Turn):
                        ShowVariants(x, y)
                        remember = [x, y]
                        for V in Variants:
                            pg.draw.circle(WIN, (200, 200, 200),
                                           (V[0] * scale + scale / 2, V[1] * scale + scale / 2), 10)
        if e.type == pg.MOUSEBUTTONUP and e.button == 1 and Turn != -1 and Turn != -2:
            x, y = (e.pos)
            x, y = math.floor(x / scale), math.floor(y / scale)
            if Variants.count([x, y]):
                Board[y][x] = Board[remember[1]][remember[0]]
                Board[remember[1]][remember[0]] = '.'

                if remember == [4, 7] and Board[y][x] == 'K0':
                    if [x, y] == [2, 7]:
                        Board[7][0] = '.'
                        Board[7][3] = 'R0'
                    if [x, y] == [6, 7]:
                        Board[7][7] = '.'
                        Board[7][5] = 'R0'
                if remember == [4, 0] and Board[y][x] == 'K1':
                    if [x, y] == [2, 0]:
                        Board[0][0] = '.'
                        Board[0][3] = 'R1'
                    if [x, y] == [6, 0]:
                        Board[0][7] = '.'
                        Board[0][5] = 'R1'

                if Board[7][0] != 'R0':
                    castlingL0 = False
                if Board[7][7] != 'R0':
                    castlingR0 = False
                if Board[7][4] != 'K0':
                    castlingL0 = False
                    castlingR0 = False
                if Board[0][0] != 'R1':
                    castlingL1 = False
                if Board[0][7] != 'R1':
                    castlingR1 = False
                if Board[0][4] != 'K1':
                    castlingL1 = False
                    castlingR1 = False
                Turn = 1 - Turn
                check = CheckCheckMate(str(Turn))
                if check == 1:
                    DrawBg()
                    DrawPieces()
                    if Turn == 0:
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'BLACK WON', False, (30, 30, 30)), (260, 310))
                    if Turn == 1:
                        WIN.blit(pg.font.SysFont(None, 30).render(
                            'WHITE WON', False, (30, 30, 30)), (260, 310))
                if check == 2:
                    WIN.blit(pg.font.SysFont(None, 30).render(
                        'DRAW', False, (30, 30, 30)), (290, 310))
                Variants = []
            if check == 0:
                DrawBg()
                DrawPieces()
            Variants = []
    display.update()
    clock.tick(60)
