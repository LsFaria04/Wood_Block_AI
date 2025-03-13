from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer
import pygame
import time

STATE_MAIN_MENU = 1
STATE_GAME_CONFIG = 2
STATE_GAME = 3
STATE_EXIT = 4

GAME_TYPE_HUMAN = 5
GAME_TYPE_AI = 6
class AppState:

    def __init__(self):
        pygame.init()
        self.state = STATE_GAME
        self.game_type = GAME_TYPE_HUMAN
        self.gui = GUI(600, 720, "Wood Block")
        self.game_state = GameState(4) # should be changed in the menu depending on the setting
        self.player = AIPlayer(1) #Use the greedy for testing

        self.dragging_piece = None
        self.drag_offset = (0, 0)

        self.start_time = None 
        self.time_taken = 0  # Time taken to complete the game

    def start_timer(self):
        if self.start_time is None:  # Only start the timer once
            self.start_time = time.time()  # 1Start the timer when the game begins

    def update_time(self):
        if self.start_time is not None:
            self.time_taken = time.time() - self.start_time

    def step(self):
        move_history = self.player.play(self.game_state)
        self.game_state.reconstruct_play(move_history, self.gui)
        if self.state == STATE_GAME:
            self.start_timer()

        self.update_time()

        # Prepare the next step in the frame
        self.gui.draw_background()
        self.game_state.draw_board(self.gui)
        self.game_state.draw_current_pieces(self.gui)

        self.gui.draw_timer(self.time_taken)

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
                self.game_state.move(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y))
                self.dragging_piece.isPlaced = True
            
            self.dragging_piece = None  # Stop dragging the piece
            self.game_state.draw_current_pieces(self.gui)

    def update_piece_position(self, x, y):
        self.dragging_piece.x = x
        self.dragging_piece.y = y
    def is_mouse_on_piece(self, piece, pos):
        return piece.x <= pos[0] <= piece.x + piece.xlen * 30 and piece.y <= pos[1] <= piece.y + piece.ylen * 30

