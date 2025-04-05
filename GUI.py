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
        self.sound_img = pygame.image.load("images/sound.png")
        self.sound_img = pygame.transform.scale(self.sound_img, (50, 50))
        self.sound_muted_img = pygame.image.load("images/sound_muted.png")
        self.sound_muted_img = pygame.transform.scale(self.sound_muted_img, (50, 50))    


    
    def __del__(self):
        pygame.quit()

    def draw_piece(self, piece, block_size):
        '''
        Draws a playable piece into the screen
        '''
        self.screen_needs_update = True
        occupied_cells = piece.getOccupiedCells()
        for (x, y) in occupied_cells:
            draw_x = piece.x + x * block_size
            draw_y = piece.y + y * block_size
            # Use stored `piece.x` and `piece.y` for drawing
            self.screen.blit(self.block_img, (draw_x, draw_y))

    def draw_highlighted_piece(self, piece, block_size):
        '''
        Draws the playable piece highlighted by the hint
        '''
        self.screen_needs_update = True
        occupied_cells = piece.getOccupiedCells()
        for (x, y) in occupied_cells:
            draw_x = piece.x + x * block_size
            draw_y = piece.y + y * block_size
            highlight_surface = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
            highlight_surface.fill((0, 255, 0, 128))  # Green with transparency
            self.screen.blit(highlight_surface, (draw_x, draw_y))

    def draw_rectangle(self, cords):
        '''
        Draws a rectangle (wood block, small portion of the piece) into the screen at the given coordinates
        '''
        self.screen_needs_update = True
        x, y = cords
        x_offset = 30
        y_offset = 30
        self.screen.blit(self.block_img, (x * x_offset, y * y_offset))

    def draw_board_background(self, cords):
        '''
        Draws a piece of the background of the board in the given coordinates (wood blocks with darker color)
        '''
        x, y = cords
        x_offset = 30
        y_offset = 30
        self.screen.blit(self.block_background, (x * x_offset, y *y_offset))

    def draw_background(self):
        '''
        Draws the background of the game (wood texture)
        '''
        self.screen.blit(self.background, (0, 0))
    
    def draw_button(self, cords, text):
        '''
        Draws a menu button in the given coordinates with the given text inside it
        '''
        x,y = cords
        self.screen.blit(self.menu_button, (x, y))
        font = pygame.font.Font(None, 42)
        text_surface = font.render(text, True, (255, 255, 255)) 
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (x + 100 - (lenx // 2), y + 35 - (leny // 2)))
    
    def draw_menu_title(self, text):
        '''
        Draws the menu title at the top of the screen using the given text
        '''
        x = 300
        y = 60

        font = pygame.font.Font(None, 100)
        text_surface = font.render(text, True, (255, 255, 255))
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (x - (lenx // 2), y - (leny // 2)))
    
    def draw_arrow_button(self, isLeft, cords):
        '''
        Draws arrow buttons (buttons to change options) at the given coordinates. Used the isLeft parameter to identify the direction of the arrow
        '''
        x,y = cords
        small_button =  pygame.transform.scale(self.menu_button_img, (50, 50))
        self.screen.blit(small_button, (x,y))
        font = pygame.font.Font(None, 48)
        font.set_bold(True)
        text_surface = font.render('>', True, (255, 255, 255)) 
        if isLeft:
            text_surface = font.render('<', True, (255, 255, 255)) 
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (x + 25 - (lenx // 2), y + 25 - (leny // 2)))
    
    def draw_option_text(self, cords, text):
        '''
        Draws the text that appears in the options selection at the given coordinates
        '''
        x,y = cords
        font = pygame.font.Font(None, 42)
        text_surface = font.render(text, True, (255, 255, 255)) 
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (155 + x - (lenx // 2), y + 25 - (leny // 2)))
    
    def draw_ai_warning(self):
        '''
        Draws a warning when the AI is playing
        '''
        font = pygame.font.Font(None, 42)
        text_surface = font.render("Ai is Calculating ...", True, (255, 255, 255)) 
        lenx,leny = text_surface.get_size()
        self.screen.blit(text_surface, (300 - (lenx // 2), 360 - (leny // 2)))
    
    def draw_above_button_text(self, cords, text, buttonSize):
        '''
        Draws the text that appears at the top of some buttons at the given coordinates.
        '''
        x,y = cords
        lenx,leny = buttonSize
        font = pygame.font.Font(None, 42)
        text_surface = font.render(text, True, (255, 255, 255)) 
        textx,texty = text_surface.get_size()
        self.screen.blit(text_surface, (x + lenx // 2 - textx // 2, y - leny + texty // 2))

    def draw_next_previous_buttons(self, current_idx, max_idx):
        '''
        Draws the next and previous buttons that appear in the Ai moves review
        '''
        if current_idx > 0:
            self.draw_arrow_button(True, (120,600))
            self.draw_above_button_text((120, 600), "Prev", (50,50))
        if (current_idx + 1) == max_idx:
            self.draw_arrow_button(False, (420, 600))
            self.draw_above_button_text((420, 600), "Stats", (50,50))
        elif (current_idx + 1) < max_idx:
            self.draw_arrow_button(False, (420, 600))
            self.draw_above_button_text((420, 600), "Next", (50,50))
        
    def draw_gameover_stats(self,cords, description, stat):
        '''
        Draws the game over screen stats (time, memory used, points, ...)
        '''
        x,y = cords
        font = pygame.font.Font(None, 42)
        text_surface = font.render(description, True, (255, 255, 255)) 
        textx,texty = text_surface.get_size()
        self.screen.blit(text_surface, (x , y))
        text_surface2 = font.render(stat, True, (0, 255, 0)) 
        self.screen.blit(text_surface2, (x + textx + 20 , y))
    
    def get_event(self):
        '''
        Gets the events captured by the pygame event (keyboard, mouse)
        '''
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
        '''
        Refreshes the screen to update the frame
        '''
        if self.screen_needs_update:
            pygame.display.flip()
            self.screen_needs_update = False

    def draw_timer(self, time_taken):
        '''
        Draws the game timer into the screen
        '''
        font = pygame.font.Font(None, 36)
        time_text = f"Time: {int(time_taken)}s"
        text_surface = font.render(time_text, True, (255, 255, 255)) 
        self.screen.blit(text_surface, (10, 5))

    def draw_hint_button(self):
        '''
        Draws the Ai hint button into the screen
        '''
        x, y = 545, 5
        self.screen.blit(self.hint_button, (x, y))

    def draw_score(self, score):
        '''
        Draws the game score into the screen during the game 
        '''
        font = pygame.font.Font(None, 36)
        score_text = f"Score: {score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        
        text_width, text_height = text_surface.get_size()
        screen_width = self.screen.get_width()
        
        x_position = (screen_width - text_width) // 2
        
        self.screen.blit(text_surface, (x_position, 5))

    def draw_mute_button(self, muted):
        '''
        Draws the mute button to stop the music during the game
        '''
        image = self.sound_muted_img if muted else self.sound_img

        x, y = 545, 60

        if muted:
            overlay = pygame.Surface((50, 50), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 100))  
            
            image_with_overlay = image.copy()
            image_with_overlay.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            self.screen.blit(image_with_overlay, (x, y))
        else:
            self.screen.blit(image, (x, y))

    def draw_highlighted_cell(self, cords):
        """ Draws a highlighted cell to indicate AI's suggested move. """
        x, y = cords
        x_offset = 30
        y_offset = 30
        
        highlight_color = (0, 255, 0, 128)  # Green with transparency
        
        # Create a surface with transparency
        highlight_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        highlight_surface.fill(highlight_color)
        
        # Blit it onto the screen at the correct position
        self.screen.blit(highlight_surface, (x * x_offset, y * y_offset))
        
        self.screen_needs_update = True
