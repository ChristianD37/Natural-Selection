from game import Game

g = Game()
g.intro.display_menu()
# Main file to loop the game
while g.running:
    # Use the menu state machine
    g.menu.display_menu()
    # If start is selected, begin the game loop
    while g.playing:
        g.reset()
        g.gameLoop()

g.quit()