import pygame

class GUI:

    def __init__(self, width, height, caption):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.screen_needs_update = True
        self.block_img = pygame.image.load("images/block.png")
        self.block_background = pygame.image.load("images/block_darker_wood.png")
        self.block_img = pygame.transform.scale(self.block_img, (30, 30))
        self.block_background = pygame.transform.scale(self.block_background, (30, 30))
        self.menu_button_img = pygame.image.load("images/wood_button.png")
        self.menu_button = pygame.transform.scale(self.menu_button_img, (200, 70))
        self.background = pygame.image.load("images/wood.jpg")
        self.background = pygame.transform.scale(self.background, (width, height))
        self.hint_button_img = pygame.image.load("images/hint.png")
        self.hint_button = pygame.transform.scale(self.hint_button_img, (50, 50))
    
    def __del__(self):
        pygame.quit()

    def drawPiece(self, piece, block_size):
        self.screen_needs_update = True
        occupied_cells = piece.getOccupiedCells()
        for (x, y) in occupied_cells:
            draw_x = piece.x + x * block_size
            draw_y = piece.y + y * block_size
            # Use stored `piece.x` and `piece.y` for drawing
            self.screen.blit(self.block_img, (draw_x, draw_y))

    def drawRectangle(self, cords):
        self.screen_needs_update = True
        x, y = cords
        x_offset = 30
        y_offset = 30
        self.screen.blit(self.block_img, (x * x_offset, y * y_offset))

    def draw_board_background(self, cords):
        x, y = cords
        x_offset = 30
        y_offset = 30
        self.screen.blit(self.block_background, (x * x_offset, y *y_offset))

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
    
    def draw_button(self, cords, text):
        x,y = cords
        self.screen.blit(self.menu_button, (x, y))
        font = pygame.font.Font(None, 42)
        text_surface = font.render(text, True, (255, 255, 255)) 
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (x + 100 - (lenx // 2), y + 35 - (leny // 2)))
    
    def draw_menu_title(self, text):
        x = 300
        y = 60

        font = pygame.font.Font(None, 100)
        text_surface = font.render(text, True, (255, 255, 255))
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (x - (lenx // 2), y - (leny // 2)))


    
    def get_event(self):
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            return 'q'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'q'
            if event.key == pygame.K_ESCAPE:
                return 'esc'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                return 'mousedown'
        elif event.type == pygame.MOUSEMOTION:
            return 'mousemove'
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                return 'mouseup'
        else:
            return None

    def refresh_screen(self):
        if self.screen_needs_update:
            pygame.display.flip()
            self.screen_needs_update = False

    def draw_timer(self, time_taken):
        font = pygame.font.Font(None, 36)
        time_text = f"Time: {int(time_taken)}s"
        text_surface = font.render(time_text, True, (255, 255, 255)) 
        self.screen.blit(text_surface, (10, 5))

    def draw_hint_button(self):
        x, y = 545, 5
        self.screen.blit(self.hint_button, (x, y))