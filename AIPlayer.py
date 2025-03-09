import numpy as np
from GameState import GameState
import heapq

class AIPlayer:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def play(self,gamestate):
        '''
        AI play. Returns the move history that lead to the solution or fail if no solution was found
        '''
        if self.algorithm == 1:
            self.bfs()
        elif self.algorithm == 2:
            self.dfs()
        elif self.algorithm == 3:
            self.iteractive_deepening()
        elif self.algorithm == 4:
            self.uniform_cost()
        elif self.algorithm == 5:
            return self.greedy(gamestate, lambda state : self.numb_pieces(state) + self.near_full_line(state) + self.occupied_space(state))
        elif self.algorithm == 6:
            self.a_star()
        elif self.algorithm == 7:
            self.a_star_weighted()
        else:
            print("Algorithm is not available")
    
    def bfs(self):
        return None
    def dfs(self):
        return None
    def iteractive_deepening(self):
        return None
    def uniform_cost(self):
        return None
    

    def greedy(self, game_state, heuristic):
        setattr(GameState, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
        visited = set()
        states = [game_state]

        while states:
            current_state = heapq.heappop(states)
            visited.add(current_state)

            if current_state.game_over() :
                return current_state.move_history

            for state in current_state.children():
                if state in visited:
                    continue
                heapq.heappush(states, state)
        return None

    def a_star(self):
        return None
    def a_star_weighted(self):
        return None
    

    def occupied_space(self, game_state):
        '''
        Determines the amount of space that is occupied and returns a cost to use as a heuristic. Less is better
        '''
        board = game_state.board
        counter = 0
        for line in board:
            for block in line:
                if block == 1:
                    counter += 1
        return counter / (len(board) * len(board[0]))
    
    def numb_pieces(self,game_state):
        '''
        Determines the number of pieces to play. Less is better
        '''
        return len(game_state.L) + len(game_state.Q) * 2
    
    def near_full_line(self,game_state):
        '''
        Determines the space left to fill a line or column. Less is better.
        It penalizes a line/column if more than half of the line is free.
        '''
        board = game_state.board
        line_numb = len(board)
        col_numb = len(board[0])
        lines = np.zeros(line_numb)
        columns = np.zeros(col_numb)

        for lin in range(line_numb):
            for col in range(col_numb):
                if board[lin][col] == 0:
                    lines[lin] += 1
                    columns[col] += 1
        
        accum = 0
        for value in lines:
            #check if the line needs to be penalized
            if value < line_numb / 2:
                accum += value
            else:
                accum += line_numb
        
        for value in columns:
            #check if the column needs to be penalized
            if value < col_numb:
                accum += value
            else:
                accum += col_numb
        
        return accum