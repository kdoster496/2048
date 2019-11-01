import random, pygame, sys
from tile import Tile, getScaledFont
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 530
WINDOWHEIGHT = 630
BOARDWIDTH = 4
BOARDHEIGHT = 4
BOXSIZE = 100
GAPSIZE = int(BOXSIZE / 10)
NOBORDER = BOXSIZE - GAPSIZE
XMARGIN = BOXSIZE / 2
YMARGIN = BOXSIZE * 3 / 2

BLACK = (0, 0, 0)
DARKGRAY = (100, 100, 100)
GRAY = (150, 150, 150)
DARKWHITE = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (100, 200, 50)
BLUE = (0, 50, 255)

BGCOLOR = GREEN
BORDERCOLOR = DARKGRAY
BOXCOLOR = GRAY
BLANKCOLOR = DARKWHITE
TEXTCOLOR = BLACK

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


def main():
    global FPSCLOCK, DISPLAYSURF, UNDO_SURF, UNDO_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')

    DISPLAYSURF.fill(BGCOLOR)
    board = makeBoard()
    newRandom(board)
    newRandom(board)
    drawGame(board)

    undoFont = getScaledFont(200, 100, 'UNDO', 'Comic Sans')
    undoText = undoFont.render('UNDO', 1, TEXTCOLOR, BOXCOLOR)
    UNDO_RECT = undoText.get_rect(center=(405, 75))
    DISPLAYSURF.blit(undoText, UNDO_RECT)
    undoBoard = makeBoard()

    while True:
        slideDirection = None
        #UNDO_SURF = DISPLAYSURF.copy()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    slideDirection = LEFT
                elif event.key in (K_RIGHT, K_d):
                    slideDirection = RIGHT
                elif event.key in (K_UP, K_w):
                    slideDirection = UP
                elif event.key in (K_DOWN, K_s):
                    slideDirection = DOWN
            elif event.type == MOUSEBUTTONDOWN and UNDO_RECT.collidepoint(event.pos):
                #DISPLAYSURF = UNDO_SURF.copy()
                #board = undoBoard
                for y, row in enumerate(undoBoard):
                    for x, val in enumerate(row):
                        board[y][x] = val
                drawGame(board)
                print('undo')

        isSlide = False
        if slideDirection == LEFT or slideDirection == UP:
            for y, row in enumerate(board):
                for x, val in enumerate(row):
                    undoBoard[y][x] = val
            for x in range(BOARDWIDTH):
                for y in range(BOARDHEIGHT):
                    if board[x][y]:
                        merge = checkForMerge(board, slideDirection, x, y)
                        farx, fary = findFarthestBlank(board, slideDirection, x, y)
                        if merge or not farx == x or not fary == y:
                            isSlide = True
                        slide(board, slideDirection, x, y, FPS, merge)
        elif slideDirection == RIGHT or slideDirection == DOWN:
            for y, row in enumerate(board):
                for x, val in enumerate(row):
                    undoBoard[y][x] = val
            for x in reversed(range(BOARDWIDTH)):
                for y in reversed(range(BOARDHEIGHT)):
                    if board[x][y]:
                        merge = checkForMerge(board, slideDirection, x, y)
                        farx, fary = findFarthestBlank(board, slideDirection, x, y)
                        if merge or not farx == x or not fary == y:
                            isSlide = True
                        slide(board, slideDirection, x, y, FPS, merge)
        if isSlide:
            newRandom(board)
        pygame.display.update()
        checkForLose(board)
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if board[x][y]:
                    board[x][y].merged = False


def makeBoard():
    board = []
    for i in range(BOARDWIDTH):
        subBoard = [None] * BOARDHEIGHT
        board.append(subBoard)
    return board


def drawGame(board):
    font = getScaledFont(200, 100, '2048', 'Comic Sans')
    text = font.render('2048', 1, BLACK)
    text_rect = text.get_rect(center=(125, 75))
    DISPLAYSURF.blit(text, text_rect)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left, top, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))
            if board[boxx][boxy]:
                DISPLAYSURF.blit(board[boxx][boxy].surface, (left + GAPSIZE, top + GAPSIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, BOXSIZE - GAPSIZE, BOXSIZE - GAPSIZE))


def slide(board, direction, startx, starty, speed, merge):
    endx, endy = findFarthestBlank(board, direction, startx, starty)
    #if endx == startx and endy == starty:
        #return None
    before = board[startx][starty]
    if direction == RIGHT:
        if merge:
            endx += 1
        for i in range(startx, endx):
            left, top = leftTopCoordsOfBox(i, starty)
            baseSurf = DISPLAYSURF.copy()
            pygame.draw.rect(baseSurf, BORDERCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(baseSurf, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))

            for j in range(GAPSIZE, BOXSIZE + GAPSIZE, speed):
                DISPLAYSURF.blit(baseSurf, (0, 0))
                drawTile(board, i, starty, j, 0)
                pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left, top, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))
                pygame.draw.rect(DISPLAYSURF, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))
                pygame.display.update()
            board[i + 1][starty] = board[i][starty]
            board[i][starty] = None
            FPSCLOCK.tick(FPS)
    elif direction == DOWN:
        if merge:
            endy += 1
        for i in range(starty, endy):
            left, top = leftTopCoordsOfBox(startx, i)
            baseSurf = DISPLAYSURF.copy()
            pygame.draw.rect(baseSurf, BORDERCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(baseSurf, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))

            for j in range(GAPSIZE, BOXSIZE + GAPSIZE, speed):
                DISPLAYSURF.blit(baseSurf, (0, 0))
                drawTile(board, startx, i, 0, j)
                pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left, top, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))
                pygame.draw.rect(DISPLAYSURF, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))
                pygame.display.update()
            board[startx][i + 1] = board[startx][i]
            board[startx][i] = None
            FPSCLOCK.tick(FPS)
    elif direction == LEFT:
        if merge:
            endx -= 1
        for i in reversed(range(endx + 1, startx + 1)):
            left, top = leftTopCoordsOfBox(i, starty)
            baseSurf = DISPLAYSURF.copy()
            pygame.draw.rect(baseSurf, BORDERCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(baseSurf, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))

            for j in range(GAPSIZE, BOXSIZE + GAPSIZE, speed):
                DISPLAYSURF.blit(baseSurf, (0, 0))
                drawTile(board, i, starty, j * -1, 0)
                pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left, top, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))
                pygame.draw.rect(DISPLAYSURF, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))
                pygame.display.update()
            board[i - 1][starty] = board[i][starty]
            board[i][starty] = None
            FPSCLOCK.tick(FPS)
    elif direction == UP:
        if merge:
            endy -= 1
        for i in reversed(range(endy + 1, starty + 1)):
            left, top = leftTopCoordsOfBox(startx, i)
            baseSurf = DISPLAYSURF.copy()
            pygame.draw.rect(baseSurf, BORDERCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(baseSurf, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))

            for j in range(GAPSIZE, BOXSIZE + GAPSIZE, speed):
                DISPLAYSURF.blit(baseSurf, (0, 0))
                drawTile(board, startx, i, 0, -1 * j)
                pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left, top, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))
                pygame.draw.rect(DISPLAYSURF, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, NOBORDER, NOBORDER))
                pygame.display.update()
            board[startx][i - 1] = board[startx][i]
            board[startx][i] = None
            FPSCLOCK.tick(FPS)

    board[startx][starty] = None
    if not merge:
        board[endx][endy] = before
    else:
        board[endx][endy] = Tile(before.numDisplay * 2, NOBORDER, BOXCOLOR, TEXTCOLOR)
        board[endx][endy].merged = True
    drawGame(board)
    pygame.display.update()


def checkForMerge(board, direction, posx, posy):
    if direction == RIGHT and not posx == BOARDWIDTH - 1:
        for boxx in range(posx + 1, BOARDWIDTH):
            if board[boxx][posy]:
                return board[boxx][posy].numDisplay == board[posx][posy].numDisplay and not board[boxx][posy].merged
    elif direction == DOWN and not posy == BOARDHEIGHT - 1:
        for boxy in range(posy + 1, BOARDHEIGHT):
            if board[posx][boxy]:
                return board[posx][boxy].numDisplay == board[posx][posy].numDisplay and not board[posx][boxy].merged
    elif direction == LEFT and not posx == 0:
        for boxx in reversed(range(posx)):
            if board[boxx][posy]:
                return board[boxx][posy].numDisplay == board[posx][posy].numDisplay and not board[boxx][posy].merged
    elif direction == UP and not posy == 0:
        for boxy in reversed(range(posy)):
            if board[posx][boxy]:
                return board[posx][boxy].numDisplay == board[posx][posy].numDisplay and not board[posx][boxy].merged
    return False


def findFarthestBlank(board, direction, posx, posy):
    if direction == RIGHT and not posx == BOARDWIDTH - 1:
        for boxx in reversed(range(posx + 1, BOARDWIDTH)):
            if board[boxx][posy] is None:
                return boxx, posy
    elif direction == DOWN and not posy == BOARDHEIGHT - 1:
        for boxy in reversed(range(posy + 1, BOARDHEIGHT)):
            if board[posx][boxy] is None:
                return posx, boxy
    elif direction == LEFT and not posx == 0:
        for boxx in range(posx):
            if board[boxx][posy] is None:
                return boxx, posy
    elif direction == UP and not posy == 0:
        for boxy in range(posy):
            if board[posx][boxy] is None:
                return posx, boxy
    return posx, posy


def drawTile(board, tilex, tiley, adjx=0, adjy=0):
    left, top = leftTopCoordsOfBox(tilex, tiley)
    DISPLAYSURF.blit(board[tilex][tiley].surface, (left + GAPSIZE + adjx, top + GAPSIZE + adjy))


def newRandom(board):
    num = random.randrange(BOARDWIDTH * BOARDHEIGHT)
    isRepeat = True
    while isRepeat:
        posx, posy = getBoardPosish(num)
        if board[posx][posy]:
            num = random.randrange(BOARDWIDTH * BOARDHEIGHT)
        else:
            isRepeat = False
    posx, posy = getBoardPosish(num)
    left, top = leftTopCoordsOfBox(posx, posy)
    disp = random.randrange(10)
    if disp == 9:
        disp = 4
    else:
        disp = 2
    board[posx][posy] = Tile(disp, NOBORDER, BOXCOLOR, TEXTCOLOR)
    DISPLAYSURF.blit(board[posx][posy].surface, (left + GAPSIZE, top + GAPSIZE))


def checkForLose(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if not board[x][y] or checkForMerge(board, LEFT, x, y) or checkForMerge(board, RIGHT, x, y) or checkForMerge(board, UP, x, y) or checkForMerge(board, DOWN, x, y):
                return False
    DISPLAYSURF.fill(BLACK)
    font = getScaledFont(WINDOWWIDTH, WINDOWHEIGHT, 'YOU LOSE', 'Comic Sans')
    text = font.render('YOU LOSE', 1, RED)
    text_rect = text.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(text, text_rect)


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + XMARGIN
    top = boxy * BOXSIZE + YMARGIN
    return left, top


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def getBoardPosish(box):
    boxx = int(box / 4)
    boxy = box % 4
    return boxx, boxy


if __name__ == '__main__':
    main()