class Menu:
    def __init__(self) :
        self.selected = -1
        self.options = ["Human", "Ai", "Exit"]
    

    def draw_menu(self, gui):
        y_space = 420 // len(self.options)
        gui.draw_menu_title("Wood Block")
        for idx, option in enumerate(self.options):
            gui.draw_button((200, (200 + y_space*idx)), option)
    
    def mouse_over_option(self, pos):
        y_space = 420 // len(self.options)
        x,y = pos
        for idx in range(len(self.options)):
            if x >= 200 and x <= 500 and y >= (200 + y_space*idx) and y <= (200 + y_space*idx + 70):
                self.selected = idx
                return
        self.selected = -1

    def mouse_down_option(self):
        if self.selected != -1:
            return self.options[self.selected]