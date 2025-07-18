class Menu:
    def __init__(self) :
        self.selected = -1

        self.current_menu = "Main"

        #Menu options
        self.main_menu_options = ["Human", "AI", "Exit"]
        self.pause_menu_options = ["Resume", "Restart", "Exit"]
        self.game_conf_selection = ["Random", "Load Config"]
        self.load_config_menu = ["Continue"]

        self.options = ["Human", "AI", "Exit"] #options in use in the current menu

        #Options in the configuration menus (options, option selected)
        self.load_conf_menu = [(["configBfs", "configDfs","configIter", "configGreed","configUcs","configAstar","configAstarw"], 0, "Configuration")]
        self.choose_conf_menu = [(["5", "10"],0,"Board Size (NxN)" ), (["6","18", "30"],0,"Number of Pieces"), (["BFS", "DFS", "Iter-Deep", "UCS", "Greedy", "A*", "A* Weighted"], 0 , "AI Algorithm"), (["Heuristic 1", "Heuristic 2", "Heuristic 3", "Heuristic 4"], 0 , "Algorithm Heuristic")]
        
        self.conf_options = self.load_conf_menu #the current conf options in use
        self.arrow_selected = (-1,-1) # Arrow Button selected (idx, isleft)

        self.config_descriptions = [
            "Board Size (NxN)",
            "Number of Pieces",
            "Hint Algorithm"
        ]
 
    def draw_menu(self, gui):
        '''
        Generic menu draw
        '''
        gui.screen_needs_update = True
        y_space = 420 // len(self.options)

        if self.current_menu == "Main":
            gui.draw_menu_title("Wood Block")

        if self.current_menu == "LoadConfig" or self.current_menu == "ChooseConfig":
            self.draw_config_menu(gui)
            return None

        for idx, option in enumerate(self.options):
            gui.draw_button((200, (200 + y_space*idx)), option)
        
        
    
    def draw_config_menu(self, gui):
        '''
        Specialized menu for configuration menus
        '''
        y_space = 500 // ((len(self.conf_options)) + 1) # space for the config selection and continue button

        for idx, config in enumerate(self.conf_options):
            options, selected, description = config
            gui.draw_option_text((150, y_space + y_space*idx - 45), description)

            gui.draw_arrow_button(True, (150, y_space + y_space*idx))
            gui.draw_arrow_button(False, (400, y_space + y_space*idx))
            
            gui.draw_option_text((150,y_space + y_space*idx),options[selected])

            if options[selected] in ["BFS", "DFS", "Iter-Deep", "UCS"] and description == "AI Algorithm":
                #Algorithms with no heuristic don't have heuristic
                break

        gui.draw_button((200, (y_space + y_space*len(self.conf_options))), "Continue")

    
    def mouse_over_option(self, pos):
        '''
        Checks if the mouse if over some option and returns the option it is selecting
        '''
        if self.current_menu == "LoadConfig" or self.current_menu == "ChooseConfig":
            self.mouse_over_option_config_menu(pos)
            return

        y_space = 420 // len(self.options)
        x,y = pos
        for idx in range(len(self.options)):
            if x >= 200 and x <= 500 and y >= (200 + y_space*idx) and y <= (200 + y_space*idx + 70):
                self.selected = idx
                return
        self.selected = -1
    
    def mouse_over_option_config_menu(self, pos):
        '''
        Checks if the mouse if over some option and returns the option it is selecting (only for the config menus)
        '''
        x,y = pos

        y_space = 500 // ((len(self.conf_options)) + 1) # space for the config selection and continue button

        for idx, config in enumerate(self.conf_options):
            if x >= 150 and x <= 200 and y >= (y_space + y_space*idx) and y <= (y_space + y_space*idx + 50):
                self.arrow_selected = (idx, True)
                return
            if x >= 400 and x <= 450 and  y >= (y_space + y_space*idx) and y <= (y_space + y_space*idx + 50):
                self.arrow_selected = (idx, False)
                return
        self.arrow_selected = (-1,-1)

        if x >= 200 and x <= 500 and y >= (y_space + y_space*len(self.conf_options)) and y <= (y_space + y_space*len(self.conf_options) + 70):
            self.selected = 0
            return
        
        self.selected = -1
        

        return None

    def mouse_down_option(self):
        '''
        Gets the option that is selected by the mouse
        '''
        if self.current_menu == "LoadConfig" or self.current_menu == "ChooseConfig":
            self.mouse_down_conf_menu(self.arrow_selected[1], self.arrow_selected[0])
        if self.selected != -1:
            return self.options[self.selected]
    
    def mouse_down_conf_menu(self, isleft, idx):
        '''
        Changes the selected config according to the mouse selection
        '''
        if idx < 0 or idx >= len(self.conf_options):
            # Invalid index, do nothing
            return

        options, selected, description = self.conf_options[idx]

        if idx == -1 or isleft is None:
            #not a valid arrow
            return 

        if isleft:
            if (selected - 1) >= 0:
                selected -=1
                self.conf_options[idx] = (options, selected, description)
        else:
            if (selected + 1) < len(options):
                selected +=1
                self.conf_options[idx] = (options, selected,description)

        return None
    
    def change_menu(self, new_menu):
        '''
        Changes to a new menu
        '''
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
            self.conf_options = self.load_conf_menu
            self.selected = -1
        if new_menu == "ChooseConfig" :
            self.current_menu = "ChooseConfig"
            self.options = self.load_config_menu
            self.conf_options = self.choose_conf_menu