from GUI import GUI
from GameState import GameState

def main():
    gui = GUI(1270, 720, "Wood Block")
    game_state = GameState(50)
    while True:   
        #gui.drawRectangle(10,10,200, 200,(0,0,255))
        game_state.drawBoard(gui)
        gui.refreshScreen()
        event = gui.getEvent()
        if(event == 'q'):
            break

    return 0

if __name__ == "__main__":
    main()