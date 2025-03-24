class TextMenu :
    def __init__(self,is_ai_stats, list_values):
        self.is_ai_stats = is_ai_stats
        self.points = list_values[0]
        self.time = list_values[1]
        if is_ai_stats:
            self.memory_usage = list_values[2]
            self.visited_states = list_values[3]
        

    def draw_text_menu(self, gui):
        gui.screen_needs_update = True
        gui.draw_menu_title("Game Over")
        y_space = 420 // 5

        gui.draw_gameover_stats((150, (100 + y_space)), "Points", str(self.points))
        gui.draw_gameover_stats((150, (100 + y_space * 2)), "Time", str(self.time))
        if self.is_ai_stats:
            gui.draw_gameover_stats((150, (100 + y_space * 3)), "Memory Usage", self.memory_usage)
            gui.draw_gameover_stats((150, (100 + y_space * 4)), "Number of Visited States", str(self.visited_states))
        
        gui.draw_button((200, (100 + y_space * 5)), "Continue")
    
    def mouse_down_option(self, cords):
        x,y = cords
        y_space = 420 // 5
        if x >= 200 and x <= 500 and y >= (100 + y_space * 5) and y <= (100 + y_space * 5 + 70):
            return "Continue"
        

        
