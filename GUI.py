import pygame

class GUI:

    def __init__(self, width, height, caption):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.block_img = pygame.image.load("block.png")
        self.block_background = pygame.image.load("block_darker_wood.png")
        self.block_img = pygame.transform.scale(self.block_img, (30, 30))
        self.block_background = pygame.transform.scale(self.block_background, (30, 30))
        self.background = pygame.image.load("wood.jpg")
        self.background = pygame.transform.scale(self.background, (width, height))
    
    def __del__(self):
        pygame.quit()

    def drawPiece(self, piece, x_offset, y_offset, block_size):
        for (x, y) in piece.getOccupiedCells():
            self.screen.blit(self.block_img, (x_offset + x * block_size, y_offset + y * block_size))

    def draw_rectangle(self, cords):
        x,y = cords
        x_offset = 30
        y_offset = 30
        self.screen.blit(self.block_img, (x * x_offset, y *y_offset))

    def draw_board_background(self, cords):
        x,y = cords
        x_offset = 30
        y_offset = 30
        self.screen.blit(self.block_background, (x * x_offset, y *y_offset))

    def draw_background(self):
        self.screen.blit(self.background, (0,0))

    def get_event(self):
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            return 'q'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'q'
            
    def refresh_screen(self):
        pygame.display.flip()


