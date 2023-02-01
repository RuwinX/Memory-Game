import random
import time

import pygame
import ctypes
from pygame import mixer

pygame.init()

# Disable windows display scaling from affecting the pygame display.
ctypes.windll.user32.SetProcessDPIAware()

pygame.mixer.pre_init(44100, 16, 2, 4096)
# background sound
mixer.music.load("../src/assets/sounds/Makaih_Beats_Nostalgia_PT_2.mp3")
mixer.music.set_volume(.04)
mixer.music.play(-1)

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


def cardHide(rectCoordinates, image):
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
            value_matrixDict[(i, j)] = pairList[index]
            index += 1


def cardReveal(rectCoordinates):
    indexTobeRevealed = list(cardSpriteLocations.keys())[list(cardSpriteLocations.values()).index(rectCoordinates)]
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), rectCoordinates)
        opacity = i
        # time.sleep(0.1)
        card = pygame.image.load("../src/assets/cards/" + letterMapDict[value_matrixDict[indexTobeRevealed]])
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
            correctSound()
            revealedTileCount = 0
            revealedPaircount += 1
            rectRemover(rectCoordinates)
            revealedTileYCoordinate = None
            revealedTileXCoordinate = None
            revealedTileValue = None
            revealedTileRectValue = None
        else:
            cardReveal(rectCoordinates)
            wrongSound()
            time.sleep(1)
            cardHide(revealedTileRectValue, "../src/assets/misc/hiddenCard.png")
            cardHide(rectCoordinates, "../src/assets/misc/hiddenCard.png")
            rectAdder(revealedTileRectValue)
            revealedTileCount = 0
            revealedTileYCoordinate = None
            revealedTileXCoordinate = None
            revealedTileValue = None
            revealedTileRectValue = None
    if revealedPaircount == 18:
        pygame.time.delay(1000)
        gameOver()


def volumeButton(xCoordinate, yCoordinate):
    muteButtonRect = pygame.Rect((20, 30), (128, 128))
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), muteButtonRect)
        opacity = i
        card = pygame.image.load("../src/assets/misc/speaker.png")
        card.set_alpha(opacity)
        screen.blit(card, (xCoordinate, yCoordinate))
        pygame.display.flip()


def hiddenCardRenderer(xCoordinate, yCoordinate):
    y = yCoordinate
    screen.set_alpha(0)
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
    board_surface = pygame.Surface.copy(screen)
    pygame.Surface.fill(screen, (0, 0, 0))
    screen.set_alpha(255)
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0))
        opacity = i
        board_surface.set_alpha(opacity)
        screen.blit(board_surface, (0, 0))
        pygame.display.flip()


def splashScreenShow():
    for i in range(255):
        # pygame.Surface.fill(screen, (0, 0, 0), ())
        pygame.Surface.fill(screen, (0, 0, 0))
        opacity = i
        # time.sleep(0.1)
        image = pygame.image.load("../src/assets/logo/SplashScreenLogo.jpg")
        image.set_alpha(opacity)
        screen.blit(image, (0, 0))
        pygame.display.flip()
    time.sleep(2)
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0))
        opacity = 255 - i
        # time.sleep(0.1)
        image = pygame.image.load("../src/assets/logo/SplashScreenLogo.jpg")
        image.set_alpha(opacity)
        screen.blit(image, (0, 0))
        pygame.display.flip()


def gameOver():
    gameOver_surface = pygame.Surface.copy(screen)
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0))
        opacity = 255 - i
        # time.sleep(0.1)
        gameOver_surface.set_alpha(opacity)
        screen.blit(gameOver_surface, (0, 0))
        pygame.display.flip()
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0))
        opacity = i
        # time.sleep(0.1)
        font = pygame.font.Font("../src/assets/font/doublepixel7.ttf", 128)
        textX = 200
        textY = 450
        gameOver_text = font.render("GAME OVER.", True, (255, 255, 255))
        gameOver_text.set_alpha(opacity)
        screen.blit(gameOver_text, (textX, textY))
        pygame.display.flip()
        running = False


def selectSound():
    selectSound = mixer.Sound("../src/assets/sounds/select.mp3")
    selectSound.play()


def correctSound():
    correctSelectSound = mixer.Sound("../src/assets/sounds/correct.ogg")
    correctSelectSound.play()


def wrongSound():
    wrongSelectSound = mixer.Sound("../src/assets/sounds/wrong.ogg")
    wrongSelectSound.play()


splashScreenShow()

hiddenCardRenderer(xPos, yPos)
volumeButton(20, 30)
running = True
pairListGenerator()
populateMatrix()
letterMapper()
#print(value_matrix)
muteButtonRect = pygame.Rect((20, 30), (128, 128))
while running:
    for event in pygame.event.get():
        # making sure the game closes when the X button is hit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePointerPosition = pygame.mouse.get_pos()
            if pygame.Rect.collidepoint(muteButtonRect, mousePointerPosition):
                if mixer.music.get_volume() == 0:
                    mixer.music.set_volume(0.04)
                    pygame.Surface.fill(screen, (0, 0, 0), muteButtonRect)
                    image = pygame.image.load("../src/assets/misc/speaker.png")
                    screen.blit(image, (20, 30))
                else:
                    mixer.music.set_volume(0)
                    pygame.Surface.fill(screen, (0, 0, 0), muteButtonRect)
                    image = pygame.image.load("../src/assets/misc/mute.png")
                    screen.blit(image, (20, 30))
            else:
                for rez in rectSpriteList:
                    if pygame.Rect.collidepoint(rez, mousePointerPosition):
                        selectSound()
                        tileSelector(rez)
    # update the display with the new screen color
    pygame.display.update()
