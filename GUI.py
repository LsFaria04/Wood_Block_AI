import pygame

class GUI:

    def __init__(self, width, height, caption):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.block_img = pygame.image.load("block.png")
        self.block_img = pygame.transform.scale(self.block_img, (30, 30))
    
    def __del__(self):
        pygame.quit()

    def drawPiece(self, piece, x_offset, y_offset, block_size):
        for (x, y) in piece.getOccupiedCells():
            self.screen.blit(self.block_img, (x_offset + x * block_size, y_offset + y * block_size))

    
    def getEvent(self):
        event = pygame.event.poll()

        if(event.type == pygame.QUIT):
            return 'q'
            
    def refreshScreen(self):
        pygame.display.flip()


