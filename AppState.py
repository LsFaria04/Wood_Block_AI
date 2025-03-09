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
        self.game_state = GameState(8) # deve ser alterado no menu dependendo da setting
        self.player = AIPlayer(5) #Use the greedy for testing

        
    
    def step(self):
        #Prepara o proximo passo no frame
        #precisa ser atualizado
        move_history = self.player.play(self.game_state)
        self.game_state.reconstruct_play(move_history, self.gui)
        while self.state != 3:
            self.game_state.draw_board(self.gui)
            self.gui.refresh_screen()
            event = self.gui.get_event()
            if(event == 'q'):
                self.state = 3

