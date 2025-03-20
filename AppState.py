from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer
from Menu import Menu
import pygame
import time

STATE_MENU = 1
STATE_GAME = 2
STATE_EXIT = 3

GAME_TYPE_HUMAN = 5
GAME_TYPE_AI = 6
class AppState:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.state = STATE_MENU
        self.game_type = GAME_TYPE_HUMAN
        self.gui = GUI(600, 720, "Wood Block")
        self.game_state = GameState(10) # should be changed in the menu depending on the setting
        self.player = AIPlayer(1) #Use the greedy for testing
        self.menu = Menu()

        self.dragging_piece = None
        self.drag_offset = (0, 0)

        self.start_time = None 
        self.time_taken = 0  # Time taken to complete the game

        self.score = 0

        self.load_music()
        self.play_music()

    def load_music(self):
        pygame.mixer.music.load("music/lock_in_song.mp3")

    def play_music(self):
        pygame.mixer.music.play(-1)

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
                    self.gui.screen_needs_update = True
                    self.menu.change_menu("GameConfig")
                elif option == "Exit":
                    self.state = STATE_EXIT

            elif self.menu.current_menu == "Pause":
                if option == "Resume":
                    self.state = STATE_GAME
                elif option == "Restart":
                    self.state = STATE_GAME
                    self.start_time = None
                    self.game_state = GameState(10)
                elif option == "Exit":
                    self.menu.change_menu("Main")
                    self.gui.screen_needs_update = True
                    self.start_time = None
                    self.game_state = GameState(10)
            
            elif self.menu.current_menu == "GameConfig":
                if option == "Random":
                    self.state = STATE_GAME
                elif option == "Load Config":
                    self.menu.change_menu("LoadConfig")
                    self.gui.screen_needs_update = True
            
            elif self.menu.current_menu == "LoadConfig":
                if option == "Continue":
                    self.state = STATE_GAME

        elif event == 'mousemove':
            pos = pygame.mouse.get_pos()
            self.menu.mouse_over_option(pos)
        if self.state == STATE_EXIT:
            pygame.quit()
    
    def step_game(self):
        if self.start_time is None:
            self.start_timer()
        self.update_time()

        # Prepare the next step in the frame
        self.gui.draw_background()
        self.game_state.draw_board(self.gui)
        self.game_state.draw_current_pieces(self.gui)
        self.gui.draw_hint_button()

        self.gui.draw_timer(self.time_taken)
        self.gui.draw_score(self.score)

        self.gui.refresh_screen()
        
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

    def handle_mousedown(self):
        # Get the position where the mouse was clicked
        pos = pygame.mouse.get_pos()
        for piece in self.game_state.L:
            for i, piece in enumerate(self.game_state.L):
                if self.is_mouse_on_piece(piece, pos):
                    if piece.isPlaced:
                        continue  # Skip this piece
                    self.dragging_piece = piece
                    self.drag_offset = (pos[0] - piece.x, pos[1] - piece.y)
                    break

    def handle_mousemove(self):
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.dragging_piece:
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

