from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer
from Menu import Menu
from FileParser import parse_config_file, store_results
from collections import deque
from TextMenu import TextMenu
import sys
import pygame
import time

STATE_MENU = 1
STATE_GAME = 2
STATE_EXIT = 3
STATE_GAMEOVER = 4

class AppState:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.state = STATE_MENU
        self.gui = GUI(600, 720, "Wood Block")
        self.game_state = GameState(10,12)  # GameState dimensions are set initially and can be updated in the menu
        self.player = AIPlayer(4) #Use the greedy for testing
        self.hint_clicked = False
        self.menu = Menu()
        self.muted = False
        self.notLoaded = True

        self.current_move = 0 #Ai Move that is being displayed
        self.visited_states = None #states visited by the AI

        self.dragging_piece = None
        self.drag_offset = (0, 0)

        self.start_time = None 
        self.time_taken = 0  # Time taken to complete the game

        self.load_music()
        self.play_music()

    def load_music(self):
        '''
        Loads the music that is played during the game.
        '''
        try:
            if not self.muted:
                pygame.mixer.music.load("music/lock_in_song.mp3")
        except pygame.error as e:
            print(f"Error loading music file: {e}")

    def play_music(self):
        '''
        Starts playing the game music.
        '''
        try:
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error playing music: {e}")

    def start_timer(self):
        '''
        Starts the time counter that is displayed during the game.
        '''
        if self.start_time is None:  # Only start the timer once
            self.start_time = time.time()  # Start the timer when the game begins

    def update_time(self):
        '''
        Updates the timer thta is displayed during the game.
        '''
        if self.start_time is not None:
            self.time_taken = time.time() - self.start_time

    def step(self):
        '''
        Executes the code of the new frame (new step).
        '''
        
        if self.state == STATE_GAME:
            self.step_game()
        elif self.state == STATE_MENU:
            self.step_menu()
        elif self.state == STATE_GAMEOVER:
            self.step_gameover()
    
    def step_menu(self):
        '''
        Step (new frame) for the menu
        '''

        #Draw the frame
        self.gui.draw_background()
        self.menu.draw_menu(self.gui)
        self.gui.refresh_screen()
        
        event = self.gui.get_event() # get the most recent event (mouse click, keyboard key press, etc...) 
        
        #Execute an action according to the event captured
        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            #Mouse click detected

            #get the option (button) select
            option = self.menu.mouse_down_option()

            if self.menu.current_menu == "Main":
                if option == "Human":
                    self.isAI = False
                    self.menu.change_menu("GameConfig")
                if option == "AI":
                    self.isAI = True
                    self.AiAlreadyPlayed = False
                    self.menu.change_menu("GameConfig")
                elif option == "Exit":
                    self.state = STATE_EXIT

            elif self.menu.current_menu == "Pause":
                if option == "Resume":
                    self.state = STATE_GAME
                elif option == "Restart":
                    self.state = STATE_GAME
                    self.start_time = None
                    self.game_state = GameState(int(self.saved_config[0]), int(self.saved_config[1]))
                elif option == "Exit":
                    self.menu.change_menu("Main")
                    self.state = STATE_MENU
                    self.gui.screen_needs_update = True
                    self.start_time = None
            
            elif self.menu.current_menu == "GameConfig":
                if option == "Random":
                    self.menu.change_menu("ChooseConfig")
                elif option == "Load Config":
                    self.menu.change_menu("LoadConfig")

            elif self.menu.current_menu == "ChooseConfig":
                if option == "Continue":
                    #save the config selected by the player in the menu to be used later (restarts, saves, etc...)
                    self.saved_config = [selected + 1 if description == "AI Algorithm" or description == "Algorithm Heuristic" else options[selected] for options, selected, description in self.menu.conf_options]
                    self.game_state = GameState(int(self.saved_config[0]), int(self.saved_config[1]))  
                    self.player = AIPlayer(self.saved_config[2], self.saved_config[3])  
                    
                    self.state = STATE_GAME  

            elif self.menu.current_menu == "LoadConfig":
                
                if option == "Continue":
                    #save the config selected by the player in the menu to be used later (restarts, saves, etc...)
                    self.saved_config = [selected + 1 if description == "AI Algorithm" or description == "Algorithm Heuristic" else options[selected] for options, selected, description in self.menu.conf_options]
                    filename = "config_files/" + self.saved_config[0] + ".txt"
                    board,pieces,points = parse_config_file(filename)

                    self.game_state.board = board
                    self.game_state.L = pieces[:3]
                    self.game_state.points = points
                    self.game_state.Q = deque()
                    for piece in pieces[3:]:
                        self.game_state.Q.append(piece)

                    self.player = AIPlayer(self.saved_config[1], self.saved_config[2])
                    

                    self.state = STATE_GAME
            

        elif event == 'mousemove':
            #Mouse movement detected
            pos = pygame.mouse.get_pos()
            self.menu.mouse_over_option(pos)
        if self.state == STATE_EXIT:
            pygame.quit()
    
    def step_gameover(self):
        '''
        Step (new frame) for the Game Over Screen
        '''

        #Draw the Game over Screen
        self.gui.draw_background()
        self.gameover_menu.draw_text_menu(self.gui)
        self.gui.refresh_screen()

        event = self.gui.get_event() # get the most recent event (mouse click, keyboard key press, etc...) 

        #Execute an action according to the event captured
        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            #Mouse click detected
            pos = pygame.mouse.get_pos()
            option = self.gameover_menu.mouse_down_option(pos)

            if option == "Continue":
                self.state = STATE_MENU
                self.menu.change_menu("Main")
            if option == "Save":
                #stores the results into a file before changing the menu
                algorithm = self.menu.conf_options[-2][0][self.saved_config[-2] - 1]
                heuristic = self.menu.conf_options[-1][0][self.saved_config[-1] - 1]
                store_results(algorithm, heuristic,self.saved_results[0], self.saved_results[1], str(self.saved_results[2]), self.saved_results[3])
                self.state = STATE_MENU
                self.menu.change_menu("Main")

        if self.state == STATE_EXIT:
            pygame.quit()

        return
    
    def step_game(self):
        '''
        Step (new frame) for the Game
        '''
        if self.game_state is None:
            print("Error: GameState is not initialized!")
            self.state = STATE_MENU  # Go back to the menu instead of crashing
            return
        
        if self.isAI :
            #The game is only played by the AI
            self.step_AI_game()
            return
    
        if self.start_time is None:
            self.start_timer()
        self.update_time()

        # Prepare the next step in the frame
        if not self.hint_clicked:
            #Draw game
            self.gui.draw_background()
            self.game_state.draw_board(self.gui)
            self.game_state.draw_current_pieces(self.gui)
            self.notLoaded = True
        else:

            if self.notLoaded:
                #The hint is not loaded. Run the algorithm
                self.gui.draw_background()
                self.gui.draw_ai_warning()
                self.gui.screen_needs_update = True
                self.gui.refresh_screen()
                self.move_history, self.visited_states = self.player.play(self.game_state)
                self.notLoaded = False

            self.gui.draw_background()
            if (len(self.game_state.move_history) < len(self.move_history)):
                #Draw board and pieces with the hint
                piece, pieceIdx, position = self.move_history[len(self.game_state.move_history)].move_made
                self.game_state.draw_board(self.gui)
                self.game_state.draw_highlighted_move(self.gui, piece, position)
                self.game_state.draw_current_pieces(self.gui)
                self.game_state.draw_highlighted_piece(self.gui, pieceIdx)

        #Draw game UI
        self.gui.draw_hint_button()
        self.gui.draw_mute_button(self.muted)
        self.gui.draw_timer(self.time_taken)
        self.gui.draw_score(self.game_state.points)
        self.gui.refresh_screen()

        #check gameover
        if self.game_state.game_over():
            self.state = STATE_GAMEOVER
            self.hint_clicked = False
            self.gameover_menu = TextMenu(False, [self.game_state.points, round(self.time_taken, 3)])
            return
        
        event = self.gui.get_event() # get the most recent event (mouse click, keyboard key press, etc...) 

        #Execute an action according to the event captured
        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            #Mouse click detected
            self.handle_mousedown()
        elif event == 'mousemove':
            #Mouse move detected
            self.handle_mousemove()
        elif event == 'mouseup':
            #Mouse button up detected
            self.handle_mouseup()
        elif event == 'esc':
            #Esc key pressed. Change to pause menu
            self.menu.change_menu("Pause")
            self.state = STATE_MENU
            self.gui.screen_needs_update = True
        if self.state == STATE_EXIT:
            pygame.quit()

    def step_AI_game(self):
        '''
        Step (new frame) for the Game solved by the AI
        '''
        if not self.AiAlreadyPlayed:
            #The ai hasn't played
            #Draw the warning (Ai is calculating...)
            self.gui.draw_background()
            self.gui.draw_ai_warning()
            self.gui.screen_needs_update = True
            self.gui.refresh_screen()
            init_time = time.time()
            #Ai solves the game
            self.move_history, self.visited_states = self.player.play(self.game_state)
            final_time = time.time() - init_time
            self.AiAlreadyPlayed = True

            #Used to store the results in a file
            self.saved_results = [self.move_history, round(final_time, 3),self.move_history[-1].points, str(sys.getsizeof(self.visited_states))]

            #Pre-load the gameover_menu
            if self.move_history is None:
                 self.gameover_menu = TextMenu(False,["No Solution","No Solution"])
                 self.state = STATE_GAMEOVER
                 return
            else:
                self.gameover_menu = TextMenu(True, [self.move_history[-1].points,round(final_time, 3), str(sys.getsizeof(self.visited_states)) + " bytes", len(self.visited_states)])


        #Draw the result
        self.gui.draw_background()
        self.move_history[self.current_move].draw_board(self.gui)
        self.move_history[self.current_move].draw_current_pieces(self.gui)
        self.gui.draw_next_previous_buttons(self.current_move, len(self.move_history))
        self.gui.refresh_screen()

        event = self.gui.get_event() # get the most recent event (mouse click, keyboard key press, etc...) 

        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            #Mouse click dectected
            self.handle_mousedown_Ai()
        if self.state == STATE_EXIT:
            pygame.quit()
        
    
    def handle_mousedown_Ai(self):
        '''
        Handles the mouse clicks in the Ai mode to check if a button was selected (next, previous and stats)
        '''
        # Get the position where the mouse was clicked
        pos = pygame.mouse.get_pos()
        x,y = pos

        #Check if is next
        if x >= 120 and x <= 170 and y >= 540 and y <= 590 and self.current_move > 0:
            self.current_move -= 1
        
        #Check if is previous
        if x >= 420 and x <= 470 and y >= 540 and y <= 590 and (self.current_move + 1) < len(self.move_history) :
            self.current_move += 1
        
        #Check if is stats
        elif x >= 420 and x <= 470 and y >= 540 and y <= 590 and (self.current_move + 1) == len(self.move_history):
            self.state = STATE_GAMEOVER
            self.current_move = 0


    def handle_mousedown(self):
        '''
        Handles the mouse clicks in the human mode to check if the hint button or the mute button were pressed
        '''
        pos = pygame.mouse.get_pos()

        #mute button
        if 545 <= pos[0] <= 595 and 60 <= pos[1] <= 110:
            self.muted = not self.muted 
            if self.muted:
                pygame.mixer.music.pause()  
            else:
                pygame.mixer.music.unpause()  
            return
        
        #hint button
        if 545 <= pos[0] <= 595 and 5 <= pos[1] <= 55:
            self.hint_clicked = not self.hint_clicked
            return

        for piece in self.game_state.L:
            if self.is_mouse_on_piece(piece, pos):
                if piece.isPlaced:
                    continue  # Skip this piece
                self.dragging_piece = piece
                self.drag_offset = (pos[0] - piece.x, pos[1] - piece.y)
                break

    def handle_mousemove(self):
        '''
        Handles the mouse movement to update the position of a piece that is being dragged
        '''
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update_piece_position(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1])

    def handle_mouseup(self):
        '''
        Handles the mouse button up. Inserts the dragging piece into the board if possible
        '''
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = round((mouse_x - self.drag_offset[0]) / 30 - self.game_state.offset_x)
            grid_y = round((mouse_y - self.drag_offset[1]) / 30 - self.game_state.offset_y)

            # Check if the position is valid for placing the piece
            if self.game_state.is_move_possible(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y)):
                self.dragging_piece.isPlaced = True
                self.game_state.move(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y))
            
            self.dragging_piece = None  # Stop dragging the piece
            self.game_state.draw_current_pieces(self.gui)

    def update_piece_position(self, x, y):
        '''
        Updates the dragging piece position
        '''
        self.dragging_piece.x = x
        self.dragging_piece.y = y
    def is_mouse_on_piece(self, piece, pos):
        '''
        Checks if the mouse is above a piece (is able to drag it)
        '''
        return piece.x <= pos[0] <= piece.x + piece.xlen * 30 and piece.y <= pos[1] <= piece.y + piece.ylen * 30

