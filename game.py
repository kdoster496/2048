import random, pygame, sys
from tile import Tile, getScaledFont
from pygame.locals import *

WINDOWWIDTH  = 530
WINDOWHEIGHT = 630
BOARDWIDTH  = 4
BOARDHEIGHT = 4
BOXSIZE = 100
GAPSIZE = BOXSIZE / 10
NOBORDER = BOXSIZE - GAPSIZE
XMARGIN = BOXSIZE / 2
YMARGIN = BOXSIZE * 3 / 2

BLACK     = (  0,   0,   0)
DARKGRAY  = (100, 100, 100)
GRAY      = (150, 150, 150)
DARKWHITE = (200, 200, 200)
WHITE     = (255, 255, 255)
GREEN     = (100, 200,  50)
BLUE      = (  0,  50, 255)

BGCOLOR = GREEN
BORDERCOLOR = DARKGRAY
BOXCOLOR = GRAY
BLANKCOLOR = DARKWHITE


def main():
    global FPSCLOCK, DISPLAYSURF, UNDO_SURF, UNDO_RECT, NEW_SURF, NEW_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')

    DISPLAYSURF.fill(BGCOLOR)
    board = makeBoard()
    drawGame(board)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif None:
                print('aarons dumb')

        pygame.display.update()


def makeBoard():
    board = []
    for i in range(BOARDWIDTH):
        subBoard = [None] * BOARDHEIGHT
        board.append(subBoard)
    print (board)
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
            pygame.draw.rect(DISPLAYSURF, BLANKCOLOR, (left + GAPSIZE, top + GAPSIZE, BOXSIZE - GAPSIZE, BOXSIZE - GAPSIZE))

    pos1 = random.randrange(BOARDWIDTH * BOARDHEIGHT)
    pos2 = random.randrange(BOARDWIDTH * BOARDHEIGHT)
    isRepeat = True
    while isRepeat:
        if pos2 == pos1:
            pos2 = random.randrange(BOARDWIDTH * BOARDHEIGHT)
        else:
            isRepeat = False
    pos1x, pos1y = getBoardPosish(pos1)
    pos2x, pos2y = getBoardPosish(pos2)
    lt1 = leftTopCoordsOfBox(pos1x, pos1y)
    lt2 = leftTopCoordsOfBox(pos2x, pos2y)
    board[pos1x][pos1y] = Tile(2, NOBORDER, BOXCOLOR, BLACK)
    board[pos2x][pos2y] = Tile(2, NOBORDER, BOXCOLOR, BLACK)
    DISPLAYSURF.blit(board[pos1x][pos1y].surface, (lt1[0] + GAPSIZE, lt1[1] + GAPSIZE))
    DISPLAYSURF.blit(board[pos2x][pos2y].surface, (lt2[0] + GAPSIZE, lt2[1] + GAPSIZE))


    #pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left1 + GAPSIZE, top1 + GAPSIZE, BOXSIZE - GAPSIZE, BOXSIZE - GAPSIZE))
    #pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left2 + GAPSIZE, top2 + GAPSIZE, BOXSIZE - GAPSIZE, BOXSIZE - GAPSIZE))


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