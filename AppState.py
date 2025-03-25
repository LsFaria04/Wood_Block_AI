from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer
from Menu import Menu
from ConfigFileParser import parse_config_file
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
        self.player = AIPlayer(1) #Use the greedy for testing
        self.menu = Menu()

        self.current_move = 0 #Ai Move that is being displayed
        self.visited_states = None #states visited by the AI

        self.dragging_piece = None
        self.drag_offset = (0, 0)

        self.start_time = None 
        self.time_taken = 0  # Time taken to complete the game

        self.load_music()
        self.play_music()

    def load_music(self):
        try:
            pygame.mixer.music.load("music/jazz.mp3")
        except pygame.error as e:
            print(f"Error loading music file: {e}")

    def play_music(self):
        try:
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error playing music: {e}")

    def start_timer(self):
        if self.start_time is None:  # Only start the timer once
            self.start_time = time.time()  # Start the timer when the game begins

    def update_time(self):
        if self.start_time is not None:
            self.time_taken = time.time() - self.start_time

    def step(self):
        
        if self.state == STATE_GAME:
            self.step_game()
        elif self.state == STATE_MENU:
            self.step_menu()
        elif self.state == STATE_GAMEOVER:
            self.step_gameover()
    
    def step_menu(self):
         # Prepare the next step in the frame
        self.gui.draw_background()

        self.menu.draw_menu(self.gui)
        self.gui.refresh_screen()
        
        event = self.gui.get_event()
        

        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
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
                    print("DEBUG: choose_conf_menu =", self.menu.choose_conf_menu)  # Debugging line
                    self.saved_config = [selected + 1 if description == "AI Algorithm" else options[selected] for options, selected, description in self.menu.conf_options]
                    print("DEBUG: saved_config =", self.saved_config)  # Debugging line
                    self.game_state = GameState(int(self.saved_config[0]), int(self.saved_config[1]))  
                    self.player = AIPlayer(self.saved_config[2])  
                    
                    self.state = STATE_GAME  

            elif self.menu.current_menu == "LoadConfig":
                
                if option == "Continue":
                    self.saved_config = [selected + 1 if description == "AI Algorithm" else options[selected] for options, selected, description in self.menu.conf_options]
                    filename = "config_files/" + self.saved_config[0] + ".txt"
                    board,pieces,points = parse_config_file(filename)

                    self.game_state.board = board
                    self.game_state.L = pieces[:3]
                    self.game_state.points = points
                    self.game_state.Q = deque()
                    for piece in pieces[3:]:
                        self.game_state.Q.append(piece)

                    self.player = AIPlayer(self.saved_config[1])
                    

                    self.state = STATE_GAME
            

        elif event == 'mousemove':
            pos = pygame.mouse.get_pos()
            self.menu.mouse_over_option(pos)
        if self.state == STATE_EXIT:
            pygame.quit()
    
    def step_gameover(self):
        self.gui.draw_background()
        self.gameover_menu.draw_text_menu(self.gui)
        self.gui.refresh_screen()

        event = self.gui.get_event()

        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            pos = pygame.mouse.get_pos()
            option = self.gameover_menu.mouse_down_option(pos)

            if option == "Continue":
                self.state = STATE_MENU
                self.menu.change_menu("Main")

        elif event == 'esc':
            self.menu.change_menu("Pause")
            self.state = STATE_MENU
            self.gui.screen_needs_update = True
        if self.state == STATE_EXIT:
            pygame.quit()

        return
    
    def step_game(self):
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
        self.gui.draw_background()
        self.game_state.draw_board(self.gui)
        self.game_state.draw_current_pieces(self.gui)
        self.gui.draw_hint_button()

        self.gui.draw_timer(self.time_taken)
        self.gui.draw_score(self.game_state.points)

        self.gui.refresh_screen()

        #check gameover
        if self.game_state.game_over():
            self.state = STATE_GAMEOVER
            self.gameover_menu = TextMenu(False, [self.game_state.points, round(self.time_taken, 3)])
            return
        
        event = self.gui.get_event()

        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            self.handle_mousedown()
        elif event == 'mousemove':
            self.handle_mousemove()
        elif event == 'mouseup':
            self.handle_mouseup()
        elif event == 'esc':
            self.menu.change_menu("Pause")
            self.state = STATE_MENU
            self.gui.screen_needs_update = True
        if self.state == STATE_EXIT:
            pygame.quit()

    def step_AI_game(self):
        if not self.AiAlreadyPlayed:
            self.gui.draw_background()
            self.gui.draw_ai_warning()
            self.gui.screen_needs_update = True
            self.gui.refresh_screen()
            init_time = time.time()
            self.move_history, self.visited_states = self.player.play(self.game_state)
            final_time = time.time() - init_time
            self.AiAlreadyPlayed = True

            #Pre-load the gameover_menu
            if self.move_history is None:
                 self.gameover_menu = TextMenu(False,["No Solution","No Solution"])
                 return
            else:
                self.gameover_menu = TextMenu(True, [self.move_history[-1].points,round(final_time, 3), str(sys.getsizeof(self.visited_states)) + " bytes", len(self.visited_states)])



        self.gui.draw_background()
        self.move_history[self.current_move].draw_board(self.gui)
        self.move_history[self.current_move].draw_current_pieces(self.gui)
        self.gui.draw_next_previous_buttons(self.current_move, len(self.move_history))
        self.gui.refresh_screen()

        event = self.gui.get_event()

        if event == 'q':
            self.state = STATE_EXIT
        elif event == 'mousedown':
            self.handle_mousedown_Ai()
        elif event == 'esc':
            self.menu.change_menu("Pause")
            self.state = STATE_MENU
            self.gui.screen_needs_update = True
        if self.state == STATE_EXIT:
            pygame.quit()
        
    
    def handle_mousedown_Ai(self):
        # Get the position where the mouse was clicked
        pos = pygame.mouse.get_pos()
        x,y = pos

        if x >= 120 and x <= 170 and y >= 540 and y <= 590 and self.current_move > 0:
            self.current_move -= 1
        if x >= 420 and x <= 470 and y >= 540 and y <= 590 and (self.current_move + 1) < len(self.move_history) :
            self.current_move += 1
        elif x >= 420 and x <= 470 and y >= 540 and y <= 590 and (self.current_move + 1) == len(self.move_history):
            self.state = STATE_GAMEOVER
            self.current_move = 0


    def handle_mousedown(self):
        # Get the position where the mouse was clicked
        pos = pygame.mouse.get_pos()
        for piece in self.game_state.L:
            if self.is_mouse_on_piece(piece, pos):
                if piece.isPlaced:
                    continue  # Skip this piece
                self.dragging_piece = piece
                self.drag_offset = (pos[0] - piece.x, pos[1] - piece.y)
                break

    def handle_mousemove(self):
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update_piece_position(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1])

    def handle_mouseup(self):
        if self.dragging_piece:
            pos = pygame.mouse.get_pos()
            grid_x = round((pos[0] - self.drag_offset[0]) / 30) - 2
            grid_y = round((pos[1] - self.drag_offset[1]) / 30) - 1

            # Check if the position is valid for placing the piece
            if self.game_state.is_move_possible(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y)):
                self.dragging_piece.isPlaced = True
                self.game_state.move(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y))
            
            self.dragging_piece = None  # Stop dragging the piece
            self.game_state.draw_current_pieces(self.gui)

    def update_piece_position(self, x, y):
        self.dragging_piece.x = x
        self.dragging_piece.y = y
    def is_mouse_on_piece(self, piece, pos):
        return piece.x <= pos[0] <= piece.x + piece.xlen * 30 and piece.y <= pos[1] <= piece.y + piece.ylen * 30

