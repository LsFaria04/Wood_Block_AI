from GUI import GUI
from GameState import GameState
from AIPlayer import AIPlayer
import pygame

class AppState:
    #state 1 -> main menu
    #state 2 -> game
    #state 3 -> Exit

    def __init__(self):
        self.state = 2
        self.gui = GUI(600, 720, "Wood Block")
        self.game_state = GameState(16) # deve ser alterado no menu dependendo da setting
        self.player = AIPlayer(5) #Use the greedy for testing

        self.dragging_piece = None
        self.drag_offset = (0, 0)
 
    def step(self):
        #Prepara o proximo passo no frame
        #precisa ser atualizado
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
                self.dragging_piece = piece
                self.drag_offset = (pos[0] - piece.x * 30, pos[1] - piece.y * 30)  # Adjust the offset
                print(f"Dragging piece {i} at position ({piece.x}, {piece.y})") 
                break

    def handle_mousemove(self):
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dragging_piece.x = (mouse_x - self.drag_offset[0]) // 30
            self.dragging_piece.y = (mouse_y - self.drag_offset[1]) // 30

    def handle_mouseup(self):
        if self.dragging_piece:
            pos = pygame.mouse.get_pos()
            # Check if the position is valid for placing the piece
            if self.game_state.is_move_possible(self.game_state.L.index(self.dragging_piece), pos):
                self.game_state.move(self.game_state.L.index(self.dragging_piece), pos)
            self.dragging_piece = None  # Stop dragging the piece

    def is_mouse_on_piece(self, piece, pos):
        piece_x = piece.x * 30 #convert pos to pixels
        piece_y  = piece.y * 30
        piece_width = piece.xlen * 30
        piece_height = piece.ylen * 30
        print(f"Mouse Position: {pos}")
        print(f"Piece Position: ({piece_x}, {piece_y}), Width: {piece_width}, Height: {piece_height}")
        # Check if the mouse click is within the piece's bounds
        return piece_x <= pos[0] <= piece_x + piece_width and piece_y <= pos[1] <= piece_y + piece_height

