import pygame

class GUI:

    def __init__(self, width, height, caption):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
    
    def __del__(self):
        pygame.quit()

    def drawRectangle(self, x, y, width, height, color):
        r,g,b = color
        pygame.draw.rect(self.screen, pygame.Color(r,g,b), pygame.Rect(x,y, width, height))
    
    def getEvent(self):
        event = pygame.event.poll()

        if(event.type == pygame.QUIT):
            return 'q'
            
    def refreshScreen(self):
        pygame.display.flip()


