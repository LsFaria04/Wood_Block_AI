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
        self.gui = GUI(1270, 720, "Wood Block")
        self.game_state = GameState(16) # deve ser alterado no menu dependendo da setting
        self.player = AIPlayer(5) #Use the greedy for testing

        self.dragging_piece = None
        self.mouse_offset = (0, 0)

        
    def step(self):
        running = True
        while running:
            self.game_state.draw_board(self.gui)
            self.gui.refresh_screen()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)

    def handle_mouse_down(self, event):
        """ Check if the player clicks on a piece and start dragging """
        for i, piece in enumerate(self.game_state.L):  # Loop over selectable pieces
            piece_rect = pygame.Rect(piece.x * 30, piece.y * 30, piece.xlen * 30, piece.ylen * 30)
            if piece_rect.collidepoint(event.pos):
                self.dragging_piece = i
                self.mouse_offset = (piece.x * 30 - event.pos[0], piece.y * 30 - event.pos[1])
                break

    def handle_mouse_motion(self, event):
        """ Move the dragged piece with the mouse """
        if self.dragging_piece is not None:
            piece = self.game_state.L[self.dragging_piece]
            piece.x = (event.pos[0] + self.mouse_offset[0]) // 30
            piece.y = (event.pos[1] + self.mouse_offset[1]) // 30

    def handle_mouse_up(self, event):
        """ Drop the piece and attempt to place it """
        if self.dragging_piece is not None:
            piece = self.game_state.L[self.dragging_piece]
            x, y = piece.x, piece.y
            
            # Validate and place the piece
            if self.game_state.is_move_possible(self.dragging_piece, (x, y)):
                self.game_state.move(self.dragging_piece, (x, y))
            else:
                print("Invalid move!")
            
            self.dragging_piece = None  # Stop dragging