class Menu:
    def __init__(self) :
        self.selected = -1

        self.current_menu = "Main"
        self.main_menu_options = ["Human", "Ai", "Exit"]
        self.pause_menu_options = ["Resume", "Restart", "Exit"]
        self.game_conf_selection = ["Random", "Load Config"]
        self.load_config_menu = ["Continue"]

        self.options = ["Human", "AI", "Exit"] #options in use in the current menu
    

    def draw_menu(self, gui):
        y_space = 420 // len(self.options)
        if self.current_menu == "Main":
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
    
    def change_menu(self, new_menu):
        if new_menu == "Main":
            self.current_menu = "Main"
            self.options = self.main_menu_options
            self.selected = -1
        if new_menu == "Pause":
            self.current_menu = "Pause"
            self.options = self.pause_menu_options
            self.selected = -1
        if new_menu == "GameConfig":
            self.current_menu = "GameConfig"
            self.options = self.game_conf_selection
            self.selected = -1
        if new_menu == "LoadConfig":
            self.current_menu = "LoadConfig"
            self.options = self.load_config_menu
            self.selected = -1

    
            

        

        