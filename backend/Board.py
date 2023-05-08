from Block import Block

class Board:
    def __init__(self):
        self.board = [[Block(1), Block(2), Block(3)],
                      [Block(4), Block(5), Block(6)],
                      [Block(7), Block(8), Block(9)]]
    

    def getBlockPositionInTheBoard(self, block):
        return (block-1)//3, (block-1)%3

    def placeOnBoard(self, row, col, value, player):
        self.board[row][col].vacant=False
        self.board[row][col].currentValue=value
        self.board[row][col].placedBy=player.name
    
    def undoPlacementOnTheCell(self, block):
        row, col = self.getBlockPositionInTheBoard(block)
        self.board[row][col].vacant=True
        self.board[row][col].currentValue=None
        self.board[row][col].placedBy=None


    def printGameBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                print(self.board[row][col].currentValue if not self.board[row][col].vacant else self.board[row][col].number, end=" ")
                print(" |", end=" ") if col!=2 else print()
                    
            if row!=2:
                print("_____________")
            print(" ")
