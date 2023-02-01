# Memory-Game
A simple memory game implementation in Python. There are two versions. A text version as well as a GUI version using pygame


Rules implemented for GUI version:

1. Board Size is fixed as a 6 x 6 grid
2. Single player only.
3. Game ends when all the matches are found.


There is also a windows Executable for the game generated via pyinstaller. To run the game standalone, download all the files from the repo and run the gameExectuable.exe from within the /src/ subfolder.


Rules implemented for text version:

1. It is a multi-player game
2. Players determine the size of the game board. The maximum size is 9 rows and 9 columns.
3. If the game board has odd number of cells, the last cell will be designated as an unused cell.
4. An unused cell has the "@" sign on its back, the rest of the cells have the "?" sign on their back.
5. The game board cells contain randomly generated pairs of letters from the alphabets.
6. Players take turn to pick two cells one after another.
7. Show the letter of the cell when a player picks a valid cell.
8. If a player picks two non-matching cells, next player gets to play, and the two non-matching cells will be hidden again.
9. If a player picks a matching pair, the matching pair stays visible, and he is allowed to continue to pick another pair.
10. When a player picks a matching pair, he is awarded one point.
11. If a player picks a cell outside the game board; or a cell that is visible; or the unused cell, he loses the turn.
12. When all the cells are opened, the game is over.
13. Shows the score of players and the winner (or winners when the game) is over.
