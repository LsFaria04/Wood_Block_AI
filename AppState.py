from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer
import pygame

STATE_MAIN_MENU = 1
STATE_GAME = 2
STATE_EXIT = 3
class AppState:

    def __init__(self):
        pygame.init()
        self.state = 2
        self.gui = GUI(600, 720, "Wood Block")
        self.game_state = GameState(16) # should be changed in the menu depending on the setting
        self.player = AIPlayer(5) #Use the greedy for testing

        self.dragging_piece = None
        self.drag_offset = (0, 0)

    def step(self):
        # Prepare the next step in the frame
        self.gui.draw_background()
        self.game_state.draw_board(self.gui)
        self.game_state.draw_current_pieces(self.gui)
        self.gui.refresh_screen()
        
        event = self.gui.get_event()

        if event == 'q':
            self.state = 3
            pygame.quit()
        elif event == 'mousedown':
            self.handle_mousedown()
        elif event == 'mousemove':
            self.handle_mousemove()
        elif event == 'mouseup':
            self.handle_mouseup()

    def handle_mousedown(self):
        # Get the position where the mouse was clicked
        pos = pygame.mouse.get_pos()
        print(f"Mouse clicked at: {pos}")

        for i, piece in enumerate(self.game_state.L):
            if self.is_mouse_on_piece(piece, pos):
                if piece.isPlaced:
                    print(f"Piece {i} is already placed, can't drag it.")
                    continue  # Skip this piece
                self.dragging_piece = piece
                self.drag_offset = (pos[0] - piece.x, pos[1] - piece.y)
                print(f"Dragging piece {i} at position ({piece.x}, {piece.y})") 
                break

    def handle_mousemove(self):
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update_piece_position(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1])

    def handle_mouseup(self):
        if self.dragging_piece:
            pos = pygame.mouse.get_pos()
            grid_x = (pos[0] - self.drag_offset[0]) // 30
            grid_y = (pos[1] - self.drag_offset[1]) // 30

            # Check if the position is valid for placing the piece
            if self.game_state.is_move_possible(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y)):
                self.game_state.move(self.game_state.L.index(self.dragging_piece), (grid_x, grid_y))
                self.dragging_piece.isPlaced = True
            self.dragging_piece = None  # Stop dragging the piece

    def update_piece_position(self, x, y):
        self.dragging_piece.x = x
        self.dragging_piece.y = y

    def is_mouse_on_piece(self, piece, pos):
        piece_x = piece.x #convert pos to pixels
        piece_y  = piece.y
        piece_width = piece.xlen * 30
        piece_height = piece.ylen * 30
        print(f"Mouse Position: {pos}")
        print(f"Piece Position: ({piece_x}, {piece_y}), Width: {piece_width}, Height: {piece_height}")
        # Check if the mouse click is within the piece's bounds
        return piece_x <= pos[0] <= piece_x + piece_width and piece_y <= pos[1] <= piece_y + piece_height

