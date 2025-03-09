from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer

class AppState:
    #state 1 -> main menu
    #state 2 -> game
    #state 3 -> Exit

    def __init__(self):
        self.state = 2
        self.gui = GUI(1270, 720, "Wood Block")
        self.game_state = GameState(50,[]) # deve ser alterado no menu dependendo da setting
        self.player = AIPlayer(5) #Use the greedy for testing

        
    
    def step(self):
        #Prepara o proximo passo no frame
        #precisa ser atualizado
        self.player.play(self.game_state)
        self.game_state.drawBoard(self.gui)
        self.gui.refreshScreen()
        event = self.gui.getEvent()
        if(event == 'q'):
            self.state = 3

