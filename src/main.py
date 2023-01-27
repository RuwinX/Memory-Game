# This is a sample Python script.
import random
from itertools import cycle

class memoryGame():
    def __init__(self):
        self.revealedTileCount = 0
        self.revealedTileXCoordinate = None
        self.revealedTileYCoordinate = None
        self.display_matrix = []
        self.value_matrix = []
        self.columnLimit = -1
        self.rowLimit = -1
        self.pairList = []
        self.oddPairs = None
        self.playerList = []
        self.gameOver = False;
        self.revealedTileValue = None
        self.playerScore = 0
        self.scoreBoard = {}
        self.pool = None
        self.currentPlayername = None
        self.revealedPaircount = 0
        self.pairCount = 0
    def print_matrix(self):
        topLabel = "    "
        for j in range(self.columnLimit):
            topLabel = topLabel + str(j) + "   "
        print(topLabel, end="")
        print("\n")
        for i in range(self.rowLimit):
            print(i, end="   ")
            for j in range(self.columnLimit):
                print(self.display_matrix[i][j], end="   ")
            print("\n")
        print("\n\n")
        self.print_matrix2()
        print("----------------------------------------------------------------------------")

    def print_matrix2(self):
        topLabel = "    "
        for j in range(self.columnLimit):
            topLabel = topLabel + str(j) + "   "
        print(topLabel, end="")
        print("\n")
        for i in range(self.rowLimit):
            print(i, end="   ")
            for j in range(self.columnLimit):
                print(self.value_matrix[i][j], end="   ")
            print("\n")

    def populateMatrix(self):
        index = 0
        for i in range(self.rowLimit):
            for j in range(self.columnLimit):
                if ((i == self.rowLimit - 1) and (j == self.columnLimit - 1)):
                    if (self.oddPairs):
                        self.value_matrix[i][j] = "@"
                        self.display_matrix[i][j] = "@"
                    else:
                        self.value_matrix[i][j] = self.pairList[index]
                        index += 1
                        self.display_matrix[i][j] = "?"
                else:
                    self.value_matrix[i][j] = self.pairList[index]
                    index += 1
                    self.display_matrix[i][j] = "?"

    def oddEvenCalculator(self):
        if ((self.rowLimit * self.columnLimit) % 2 != 0):
            return True
        else:
            return False

    def pairListGenerator(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if (self.oddPairs):
            self.pairCount = ((self.rowLimit * self.columnLimit) - 1) / 2
        else:
            self.pairCount = (self.rowLimit * self.columnLimit) / 2
        for i in range(int(self.pairCount)):
            self.pairList.append(random.choice(alphabet))
        self.pairList.extend(self.pairList)
        random.shuffle(self.pairList)
        print(self.pairList)

    def playerListGenerator(self):
        self.playerList = str(input("Enter the player names separated with a comma(,) \n\n")).split(',')
        for playerName in self.playerList:
            self.scoreBoard[playerName]=0
        print(self.scoreBoard)
        self.pool=cycle(self.playerList)
        self.currentPlayername = next(self.pool)

    def gameFlowStartLogic(self):
        self.oddPairs = self.oddEvenCalculator()
        self.pairListGenerator()
        self.display_matrix = [[None for i in range(self.columnLimit)] for j in range(self.rowLimit)]
        self.value_matrix = [[None for i in range(self.columnLimit)] for j in range(self.rowLimit)]
        self.populateMatrix()
        self.gameFlowLogic()

    def gameFlowLogic(self):
        while(self.revealedPaircount != self.pairCount):
            self.print_matrix()
            self.tileSelector()
        print("all tiles revealed! Game over:")
        self.finalScoreBoard()

    def finalScoreBoard(self):
        for playerName in self.playerList:
            print(playerName,"  :  ",self.scoreBoard.get(playerName,"\n"))
        restartGame=str(input("\n do you want to restart the game? Y/N?"))
        if(restartGame=='Y'or 'y' or 'yes'):
            obj2 = memoryGame()
            obj2.gameStart()
        else:
            print("Thanks for Playing!")

    def boardSizeGenerator(self):
        boardSize = str(input("Enter the size of the board \n\n"))
        self.rowLimit = int(boardSize[0])
        self.columnLimit = int(boardSize[1])
        if ((self.rowLimit > 0) and (self.rowLimit <= 9) and (self.columnLimit > 0) and (self.columnLimit <= 9)):
            self.gameFlowStartLogic()
        else:
            print("size of the board can be a maximum of 9x9")
            self.boardSizeGenerator()

    def gameStart(self):
        print("Welcome to the memory Game: \n\n")
        self.playerListGenerator()
        self.boardSizeGenerator()


    def tileSelector(self):
        print(self.currentPlayername)
        tileSelected = str(input("Enter the tile to reveal \n"))
        xCoordinate = int(tileSelected[0])
        yCoordinate = int(tileSelected[1])
        if (((xCoordinate >= 0) and (xCoordinate <= self.rowLimit) and (yCoordinate >= 0) and (xCoordinate <= self.columnLimit))and (self.display_matrix[xCoordinate][yCoordinate] != "@") ):
            if ((self.display_matrix[xCoordinate][yCoordinate] == "?") ):
                if(self.revealedTileCount == 0):
                    self.revealedTileCount += 1
                    self.revealedTileValue = self.value_matrix[xCoordinate][yCoordinate]
                    self.display_matrix[xCoordinate][yCoordinate] = self.value_matrix[xCoordinate][yCoordinate]
                    self.revealedTileXCoordinate=xCoordinate
                    self.revealedTileYCoordinate=yCoordinate
                else:
                    if(self.revealedTileValue == self.value_matrix[xCoordinate][yCoordinate]):
                        self.display_matrix[xCoordinate][yCoordinate] = self.value_matrix[xCoordinate][yCoordinate]
                        self.revealedTileCount = 0
                        self.revealedPaircount +=1
                        self.scoreBoard[self.currentPlayername] = self.scoreBoard.get(self.currentPlayername) + 1

                    else:
                        self.display_matrix[xCoordinate][yCoordinate] = self.value_matrix[xCoordinate][yCoordinate]
                        self.print_matrix()
                        print("\n moving onto the next player")
                        self.display_matrix[self.revealedTileXCoordinate][self.revealedTileYCoordinate] = "?"
                        self.display_matrix[xCoordinate][yCoordinate] = "?"
                        self.revealedTileCount = 0
                        self.revealedTileYCoordinate = None
                        self.revealedTileXCoordinate = None
                        self.revealedTileValue = None
                        self.currentPlayername = next(self.pool)

            else:
                print("You've selected an already revealed tile, your turn is being skipped. Onto the next player")
                self.currentPlayername = next(self.pool)

        else:
            print("You've selected a wrong tile, your turn is being skipped")
            self.currentPlayername = next(self.pool)



if __name__ == '__main__':
   obj = memoryGame()
   obj.gameStart()