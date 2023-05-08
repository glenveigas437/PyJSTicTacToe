from Game import Game

game = Game()
winner = game.main()

if not winner:
    print("Game Draw")
else:
    print(f"{winner.name} has won the Game")
