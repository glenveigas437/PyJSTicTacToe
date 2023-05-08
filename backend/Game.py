from Player import Player
from Board import Board
from Checked import Checked

class Game:
    def __init__(self):
        self.winner = None
        self.gameBoard = Board()
        self.checkedLine = False
    
    def getPlayerReady(self, playerName):
        if not playerName:
            return Player('CPU', 'CPU')
        else:
            return Player(playerName, 'Human')

    
    def main(self):
        playerName1, playerName2 = None, None
        playerName1 = str(input("Enter Player Name: "))
        if playerName1 == "":
            playerName1 = None
        print(playerName1)
        playerName2 = str(input("Enter Player2 Name: "))
        if playerName2 == "":
            playerName2 = None
        if not playerName1:
            while not playerName2:
                playerName2 = input("Enter Player2 Name: ", default=None)
        
        player1 = self.getPlayerReady(playerName1)
        player2 = self.getPlayerReady(playerName2)

        return self.beginGame(player1, player2)

    def checkPlayerMoveValidity(self, number):
        row, col = self.gameBoard.getBlockPositionInTheBoard(number)
        if 1<=number<10:
            if 0<=row<3 and 0<=col<3:
                return True if self.gameBoard.board[row][col].getVacantStatus() else False
        return False
    
    def penalisePlayer(self, player):
        player.foulPlay+=1
        print('You have been Penalised, Please add a legal move!')
        if player.foulPlay!=3:
            print(f'if you make {3-player.foulPlay} more illegal moves, The other player will win the Game.')
    
    def checkSimilarity(self, array, object):
        simlarityCount=0
        for element in array:
            row, col = self.gameBoard.getBlockPositionInTheBoard(element)
            row, col = int(row), int(col)
            if self.gameBoard.board[row][col].currentValue == object:
                simlarityCount+=1
            else:
                break
        
        return True if simlarityCount==3 else False

    def playerMoving(self, player, symbol):
        legalMove = False
        while(not legalMove and player.foulPlay!=3):
            blockNumber = int(input("Enter Block Number in between 1-9"))
            playerValidity = self.checkPlayerMoveValidity(blockNumber)
            if not playerValidity:
                legalMove = False
                self.penalisePlayer(player)
            else:
                legalMove = True
        
        return blockNumber if player.foulPlay<3 else -1


    def gameCheck(self, object):
        topCheck=Checked('topCheck', [1,2,3])
        middleCheck=Checked('middleCheck', [4,5,6])
        bottomCheck=Checked('bottomCheck', [7,8,9])
        leftCheck=Checked('leftCheck', [1,4,7])
        midDownCheck=Checked('midDownCheck', [2,5,8])
        rightCheck=Checked('rightCheck', [3,6,9])
        DiagonalLR=Checked('DiagonalLR', [1,5,9])
        DiagonalRL=Checked('DiagonalRL', [3,5,7])

        checksArray=[topCheck, middleCheck, bottomCheck, leftCheck, midDownCheck, rightCheck, DiagonalLR, DiagonalRL]
        
        for check in checksArray:
            if self.checkSimilarity(check.array, object):
                self.checkedLine = check.name
                return True
        
        return False
    
    def checkDraw(self):
        for row in range(3):
            for col in range(3):
                if(self.gameBoard.board[row][col].vacant):
                    return False
        
        return True
    
    
    def automatedMove(self, player, opponent, symbol):
        highestScore = -float('inf')
        bestMove = 0

        for block in range(1, 10):
            row, col = self.gameBoard.getBlockPositionInTheBoard(block)
            row, col = int(row), int(col)
            if (self.gameBoard.board[row][col].vacant):
                self.gameBoard.placeOnBoard(row, col, symbol, player)
                score = self.minimaxAI(1, False, symbol, player, opponent)    
                self.gameBoard.undoPlacementOnTheCell(block)

                if (score > highestScore):
                    highestScore = score
                    bestMove = block

        return bestMove
        
    def minimaxAI(self, playerMoveBlock, isMaximizing, symbol, player, opponent):
        if playerMoveBlock>9:
            return 
        antisymbol = '0' if symbol=='X' else 'X'
        if (self.gameCheck(symbol)):
            return 1
        elif (self.gameCheck(antisymbol)):
            return -1
        elif(self.checkDraw()):
            return 0

        if (isMaximizing):
            bestScore = -float('inf')
            for block in range(1, 10):
                row, col = self.gameBoard.getBlockPositionInTheBoard(block)
                row, col = int(row), int(col)
                if (self.gameBoard.board[row][col].vacant):
                    self.gameBoard.placeOnBoard(row, col, symbol, player)
                    score = self.minimaxAI(playerMoveBlock+1, False, symbol, player, opponent)    
                    self.gameBoard.undoPlacementOnTheCell(block)
                    score = -float('inf') if score is None else score
                    if (score > bestScore):
                        bestScore = score
            return bestScore

        else:
            bestScore = float('inf')
            for block in range(1, 10):
                row, col = self.gameBoard.getBlockPositionInTheBoard(block)
                row, col = int(row), int(col)
                if (self.gameBoard.board[row][col].vacant):
                    self.gameBoard.placeOnBoard(row,col, antisymbol, opponent)
                    score = self.minimaxAI(playerMoveBlock+1, True, antisymbol, opponent, player)    
                    self.gameBoard.undoPlacementOnTheCell(block)
                    score = float('inf') if score is None else score
                    if (score < bestScore):
                        bestScore = score
            return bestScore
    
    def beginGame(self, player1, player2):
        gameMoves = 0
        while(gameMoves<9):
            if gameMoves==0:
                self.gameBoard.printGameBoard()


            if player1.name!='CPU':
                player1Move=self.playerMoving(player1, 'X')

                if player1Move==-1:
                    self.winner = player2
                    break
            else:
                player1Move = self.automatedMove(player1, player2, 'X')
            
            if self.winner == player2:
                break
            
            rowPlace, colPace = self.gameBoard.getBlockPositionInTheBoard(player1Move)
            self.gameBoard.placeOnBoard(rowPlace, colPace, 'X', player1)

            print("Game Board Now: ")
            self.gameBoard.printGameBoard()
            gameMoves+=1

            if gameMoves>=5:
                if self.gameCheck('X'):
                    self.winner = player1
                    break

            if gameMoves==9:
                break      

            if player2.name!='CPU':
                player2Move=self.playerMoving(player2, '0')

                if player2Move==-1:
                    self.winner = player1
                    break
            else:
                player2Move = self.automatedMove(player2, player1, '0')

            if self.winner == player1:
                break
            
            rowPlace, colPace = self.gameBoard.getBlockPositionInTheBoard(player2Move)
            print('Player 2 Moved: ', player2Move)
            self.gameBoard.placeOnBoard(rowPlace,colPace, '0', player2)

            print("Game Board Now: ")
            self.gameBoard.printGameBoard()
            gameMoves+=1

            if gameMoves>=5:
                if self.gameCheck('0'):
                    self.winner = player2
                    break
        
        return self.winner

