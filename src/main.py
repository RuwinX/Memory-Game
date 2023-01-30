import random
import time

import pygame
import ctypes

pygame.init()

# Disable windows display scaling from affecting the pygame display.
ctypes.windll.user32.SetProcessDPIAware()

# set the screen size
screen = pygame.display.set_mode((908, 1058))
# set the window caption
pygame.display.set_caption("Memory Mania")
# set the logo in the window game
xPos = 20
yPos = 170

logo = pygame.image.load("../src/assets/logo/memory-loss.png")
pygame.display.set_icon(logo)

cardSpriteLocations = {}
rectSpriteList = []

pairList = []
letterMapDict = {}
value_matrixDict = {}
value_matrix = [[None for i in range(6)] for j in range(6)]
revealedTileCount = 0
revealedTileValue = ""
revealedPaircount = 0
revealedTileRectValue = pygame.Rect


def rectRemover(rectCoordinates):
    rectSpriteList.remove(rectCoordinates)
def rectAdder(rectCoordinates):
    rectSpriteList.append(rectCoordinates)

def letterMapper():
    with open("../src/assets/imageMapper.txt") as f:
        for line in f:
            (key, val) = line.split()
            letterMapDict[str(key)] = val
def pairListGenerator():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    listOfAlphabet = []
    for i in range(len(alphabet)):
        listOfAlphabet.append(alphabet[i])
    random.shuffle(listOfAlphabet)
    random.shuffle(listOfAlphabet)
    for i in range(18):
        index = random.randrange(len(listOfAlphabet))
        pairList.append(random.choice(listOfAlphabet[index]))
        del listOfAlphabet[index]
    pairList.extend(pairList)
    random.shuffle(pairList)



def cardHide(rectCoordinates,image):
    indexTobeRevealed = list(cardSpriteLocations.keys())[list(cardSpriteLocations.values()).index(rectCoordinates)]
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), rectCoordinates)
        opacity = 255 - i
        # time.sleep(0.1)
        card = pygame.image.load(image)
        card.set_alpha(opacity)
        screen.blit(card, (rectCoordinates.left, rectCoordinates.top))
        pygame.display.flip()

def cardHide2(rectCoordinates,image):

    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), rectCoordinates)
        opacity = i
        # time.sleep(0.1)
        card = pygame.image.load(image)
        card.set_alpha(opacity)
        screen.blit(card, (rectCoordinates.left, rectCoordinates.top))
        pygame.display.flip()
def populateMatrix():
    index = 0
    for i in range(6):
        for j in range(6):
                value_matrix[i][j] = pairList[index]
                value_matrixDict[(i,j)] = pairList[index]
                index += 1


def cardReveal(rectCoordinates):
    indexTobeRevealed = list(cardSpriteLocations.keys())[list(cardSpriteLocations.values()).index(rectCoordinates)]
    #the coordinates
    #print(indexTobeRevealed) -- (0,0)
    #the letter
    #value_matrixDict[indexTobeRevealed] -- m
    # the mapping to asset
    #letterMapDict[value_matrixDict[indexTobeRevealed]]
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), rectCoordinates)
        opacity = i
        # time.sleep(0.1)
        card = pygame.image.load("../src/assets/cards/"+letterMapDict[value_matrixDict[indexTobeRevealed]])
        card.set_alpha(opacity)
        screen.blit(card, (rectCoordinates.left, rectCoordinates.top))
        pygame.display.flip()


def tileSelector(rectCoordinates):
    global revealedTileCount
    global revealedTileValue
    global revealedPaircount
    global revealedTileRectValue
    indexTobeRevealed = list(cardSpriteLocations.keys())[list(cardSpriteLocations.values()).index(rectCoordinates)]
    # the coordinates
    # print(indexTobeRevealed) -- (0,0)
    # the letter
    # value_matrixDict[indexTobeRevealed] -- m
    # the mapping to asset
    # letterMapDict[value_matrixDict[indexTobeRevealed]]
    # training_data_x = [x[0] for x in indexTobeRevealed]
    # print(training_data_x)
    xCoordinate = indexTobeRevealed[0]
    yCoordinate = indexTobeRevealed[1]
    if revealedTileCount == 0:
        revealedTileCount += 1
        revealedTileValue = value_matrix[xCoordinate][yCoordinate]
        revealedTileXCoordinate = xCoordinate
        revealedTileYCoordinate = yCoordinate
        revealedTileRectValue = rectCoordinates.copy()
        rectRemover(rectCoordinates)
        cardReveal(rectCoordinates)
    else:
        if (revealedTileValue == value_matrix[xCoordinate][yCoordinate]):
            cardReveal(rectCoordinates)
            revealedTileCount = 0
            revealedPaircount += 1
            rectRemover(rectCoordinates)
            revealedTileYCoordinate = None
            revealedTileXCoordinate = None
            revealedTileValue = None
            revealedTileRectValue = None
        else:
            cardReveal(rectCoordinates)
            time.sleep(1)
            cardHide2(revealedTileRectValue,"../src/assets/misc/hiddenCard.png")
            print("hiding tile coordinate:", rectCoordinates)
            cardHide2(rectCoordinates,"../src/assets/misc/hiddenCard.png")
            rectAdder(revealedTileRectValue)

            revealedTileCount = 0
            revealedTileYCoordinate = None
            revealedTileXCoordinate = None
            revealedTileValue = None
            revealedTileRectValue = None


def hiddenCardRenderer(xCoordinate, yCoordinate):
    y = yCoordinate
    for i in range(0, 6):
        x = xCoordinate
        for j in range(0, 6):
            card = pygame.image.load("../src/assets/misc/hiddenCard.png")
            screen.blit(card, (x, y))
            cardSpriteLocations[(i, j)] = pygame.Rect((x, y), (128, 128))
            rectSpriteList.append(pygame.Rect((x, y), (128, 128)))
            # 128 is the card dimension + 20 more for padding
            x = x + 148
        y = y + 148


hiddenCardRenderer(xPos, yPos)
running = True
#print(rectSpriteList)
#print(cardSpriteLocations)
pairListGenerator()
populateMatrix()
letterMapper()
#print(letterMapDict)
print(value_matrix)
#print(value_matrixDict)

while running:
    # change the screen color to a rgb value
    # screen.fill((160, 160, 160))
    for event in pygame.event.get():
        # making sure the game closes when the X button is hit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePointerPosition = pygame.mouse.get_pos()
            for rez in rectSpriteList:
                if pygame.Rect.collidepoint(rez, mousePointerPosition):
                    #cardReveal(rez)
                    tileSelector(rez)
                    #cardHide(rez)

    # update the display with the new screen color
    pygame.display.update()
