from GUI import GUI
from Piece import Piece
from PieceFactory import PieceFactory
from GameState import GameState

def main():
    gui = GUI(1270, 720, "Wood Block")
    game_state = GameState(30)
    while True:   
        game_state.drawBoard(gui)
        gui.refreshScreen()
        event = gui.getEvent()
        if(event == 'q'):
            break


if __name__ == "__main__":
    main()