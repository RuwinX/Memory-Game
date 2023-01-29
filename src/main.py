import pygame
import ctypes

pygame.init()

#Disable windows display scaling from affecting the pygame display.
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

cardSpriteLocations={}
rectSpriteList = []
def cardReveal(xCoordinate,yCoordinate):
    a = pygame.image.load("A.png")
    screen.blit(a, (xCoordinate, yCoordinate))

def hiddenCardRenderer(xCoordinate,yCoordinate):
    y = yCoordinate
    for i in range(0,6):
        x = xCoordinate
        for j in range(0,6):
            #pygame.Surface.fill(screen, (160, 160, 160), pygame.Rect((x, y), (128, 128)))
            card = pygame.image.load("../src/assets/misc/hiddenCard.png")
            screen.blit(card, (x,y ))
            cardSpriteLocations[(i,j)] = pygame.Rect((x, y), (128, 128))
            rectSpriteList.append(pygame.Rect((x, y), (128, 128)))
            # 128 is the card dimension + 20 more for padding
            x = x + 148
        y = y + 148


hiddenCardRenderer(xPos,yPos)
running = True
print(cardSpriteLocations)

while running:
    # change the screen color to a rgb value
    #screen.fill((160, 160, 160))

    for event in pygame.event.get():
        # making sure the game closes when the X button is hit
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePointerPosition = pygame.mouse.get_pos()
            print(mousePointerPosition)
            for rez in rectSpriteList:
                if pygame.Rect.collidepoint(rez,mousePointerPosition):
                    print("VALID!")
                    pygame.Surface.fill(screen, (160,160,160),rez)
                    print(rez)
            #cardReveal(20,170)
    # update the display with the new screen color

    pygame.display.update()
