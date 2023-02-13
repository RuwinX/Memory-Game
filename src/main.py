import random
import time

import pygame
import ctypes
from pygame import mixer

pygame.init()

# Disable windows display scaling from affecting the pygame display. Remove this line if you want display scaling to affect.
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

#This function is used to remove a specific rect from the list to remove any further collision events for it from being detected.
def rectRemover(rectCoordinates):
    rectSpriteList.remove(rectCoordinates)

#This function is to re-add a specific rect which was removed from the rectList of sprites in case an uneven pair was discovered.
def rectAdder(rectCoordinates):
    rectSpriteList.append(rectCoordinates)

#This function maps the asset value between the letters and their corresponding assets from the text file
def letterMapper():
    with open("../src/assets/imageMapper.txt") as f:
        for line in f:
            (key, val) = line.split()
            letterMapDict[str(key)] = val


#This function is used to randomize 18 letters from the 26 letter alphabet to form pairs  with no repetitions.
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

#This function is used to hide the image displayed at a specific rect and replace it with the image provided.
def cardHide(rectCoordinates, image):
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), rectCoordinates)
        opacity = i
        # time.sleep(0.1)
        card = pygame.image.load(image)
        card.set_alpha(opacity)
        screen.blit(card, (rectCoordinates.left, rectCoordinates.top))
        pygame.display.flip()

#This function is used to populate a 6x6 matrix with the random generated pairings of the 18 different alphabet pairs from  =pairListGenerator()
def populateMatrix():
    index = 0
    for i in range(6):
        for j in range(6):
            value_matrix[i][j] = pairList[index]
            value_matrixDict[(i, j)] = pairList[index]
            index += 1

#This function is used to animate and reveal the asset linked behind the card RECT to the corresponding letter from the valueMatrix. Eg- the Rect contains the letter A. The asset image for A is revealed.
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

#This function is used to reveal the identify the tile to be revealed based on the Rect Coordinates. Depending on the situation, either the card is revealed[if its the first card[, revealed and then hidden, in case is the second card to be revealed and both cards are not a match, the card is the second card to be revealed and they are both a match.
def tileSelector(rectCoordinates):
    global revealedTileCount
    global revealedTileValue
    global revealedPaircount
    global revealedTileRectValue
    indexTobeRevealed = list(cardSpriteLocations.keys())[list(cardSpriteLocations.values()).index(rectCoordinates)]
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

#This function handles the toggling on/off of the background music when the volume icon is selected.
def volumeButton(xCoordinate, yCoordinate):
    muteButtonRect = pygame.Rect((20, 30), (128, 128))
    for i in range(255):
        pygame.Surface.fill(screen, (0, 0, 0), muteButtonRect)
        opacity = i
        card = pygame.image.load("../src/assets/misc/speaker.png")
        card.set_alpha(opacity)
        screen.blit(card, (xCoordinate, yCoordinate))
        pygame.display.flip()

#this function is used to render the initial 6x6 grid with the card logo at the start of the game
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

#This function is used to display the splash screen logo at the start of the game.
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

#This function is called to display the game over screen
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

#this function is used to play the sound effect when a card is selected to be revealed.
def selectSound():
    selectSound = mixer.Sound("../src/assets/sounds/select.mp3")
    selectSound.play()

#this function is used to play the sound effect when the second card selected to be revealed, is a match to the first card revealed.
def correctSound():
    correctSelectSound = mixer.Sound("../src/assets/sounds/correct.ogg")
    correctSelectSound.play()

#this function is used to play the sound effect when the second card selected to be revealed, is not a match to the first card revealed.
def wrongSound():
    wrongSelectSound = mixer.Sound("../src/assets/sounds/wrong.ogg")
    wrongSelectSound.play()

#basic gameplay loop
splashScreenShow()
hiddenCardRenderer(xPos, yPos)
volumeButton(20, 30)
running = True
pairListGenerator()
populateMatrix()
letterMapper()
#print(value_matrix)
muteButtonRect = pygame.Rect((20, 30), (128, 128))
#main game logic loop
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
