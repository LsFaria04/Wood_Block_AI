import numpy as np
from collections import deque
from GameState import GameState
import heapq

class AIPlayer:
    def __init__(self, algorithm, heuristic = 1):
        self.algorithm = algorithm
        
        if heuristic == 1:
            self.heuristic = self.heuristic1
        elif heuristic == 2:
            self.heuristic = self.heuristic2
        elif heuristic == 3:
            self.heuristic = self.heuristic3
        elif heuristic == 4:
            self.heuristic = self.heuristic4


    def play(self,gamestate):
        '''
        AI play. Returns the move history that lead to the solution or fail if no solution was found
        '''
        if self.algorithm == 1:
            return self.bfs(gamestate)
        elif self.algorithm == 2:
            return self.dfs(gamestate)
        elif self.algorithm == 3:
            return self.iterative_deepening(gamestate)
        elif self.algorithm == 4:
            return self.uniform_cost(gamestate)
        elif self.algorithm == 5:
            return self.greedy(gamestate, self.heuristic)
        elif self.algorithm == 6:
            return self.a_star(gamestate, self.heuristic)
        elif self.algorithm == 7:
            #used the board plus the number of pieces as the weight in the algorithm, so that the heuristic weight is proportional to the size of the game 
            return self.a_star_weighted(gamestate, self.heuristic, (len(gamestate.board) + len(gamestate.Q) + len(gamestate.L)))
        else:
            print("Algorithm is not available")

    def bfs(self, gamestate):
        '''
        Bfs algorithm to solve the game. Uses a deque to store the nodes that weren't visited and a set to store the visited ones
        '''
        queue = deque([gamestate])          # initialize the queue to store the nodes
        visited = set()

        while queue:
            state = queue.popleft()
            visited.add(state) 
                                    # get first element in the queue
            if state.game_over_AI():
                (state.move_history, visited)      # check goal state

            for childState in state.children():
                if (childState not in visited):
                    queue.append(childState)
                    
        return None
    
    def dfs(self, gamestate):
        '''
        Dfs algorithm to solve the game. Uses a list as a stack to store the nodes that weren't visited and a set to store the visited ones.
        '''
        stack = [gamestate]
        visited = set()

        while stack:
            state = stack.pop()

            if state not in visited:
                visited.add(state)

            if state.game_over_AI():
                return (state.move_history, visited)
            
            for child_state in state.children():
                if child_state in visited:
                    continue
                stack.append(child_state)
        return None
    
    def depth_limited_search(self, gamestate, max_depth):
        '''
        Depth limited search algorithm to solve the game. Uses a list as a stack to store a pair (unvisited node, depth)  and a set to store the visited nodes.
        '''
        stack = [(gamestate, 0)]
        visited = set()

        while stack:
            state, depth = stack.pop()

            if state in visited:
                continue
            visited.add(state)

            if state.game_over():
                return (state.move_history, visited)

            if depth < max_depth:
                for child_state in state.children():
                    if child_state not in visited:
                        stack.append((child_state, depth + 1))

        return None
    
    def iterative_deepening(self, gamestate):
        '''
        Iterative deepening algorithm to solve the game. Uses the depth limited search but increasing the depth at each iteration
        '''
        depth = 0

        while True:
            print(f"Visiting depth {depth}")
            result = self.depth_limited_search(gamestate, depth)

            if result is not None:
                return result
            depth += 1
    
    def uniform_cost(self,gamestate):
        setattr(GameState, "__lt__", lambda self, other: other.points < self.points)
        states = []  # Min-heap for UCS
        heapq.heappush(states, (0, gamestate))
        visited = set()

        while states:
            cost, current_state = heapq.heappop(states)
            visited.add(current_state)
            if current_state.game_over_AI() :
                return (current_state.move_history, visited)
            
            for childState in current_state.children():
                if childState in visited:
                    continue
                heapq.heappush(states, (-childState.points + cost, childState))

        return None

    def greedy(self, game_state, heuristic):
        setattr(GameState, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
        visited = set()
        states = [game_state]

        while states:
            current_state = heapq.heappop(states)
            visited.add(current_state)

            if current_state.game_over_AI() :
                return (current_state.move_history, visited)
            
            for state in current_state.children():
                if state in visited:
                    continue
                heapq.heappush(states, state)

        return None

    def a_star(self, game_state, heuristic):
        #Uses the game points as the cost of a state. More points mean less cost
        return self.greedy(game_state, lambda state : sum([-game_state.points for game_state in state.move_history ]) + heuristic(state))
    
    def a_star_weighted(self, game_state, heuristic, weight):
         #adds a weight to the heuristic
         return self.greedy(game_state, lambda state : sum([-game_state.points for game_state in state.move_history ]) + weight * heuristic(state))
    

    def occupied_space(self, board):
        '''
        Determines the amount of space that is occupied and returns a cost to use as a heuristic. Less is better
        '''
        counter = 0
        for line in board:
            for block in line:
                if block == 1:
                    counter += 1
        return counter
    
    def near_full_line(self,board):
        '''
        Determines the space left to fill a line or column. Less is better.
        It penalizes a line/column if more than half of the line is free.
        '''
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
            if value > col_numb / 2:
                accum += value
        
        for value in columns:
            #check if the column needs to be penalized
            if value > line_numb / 2:
                accum += value
        
        return accum
    

    def heuristic1(self, gamestate):
        # Gives more weight to the obtention of points.
        # The near_full_line function give more weight to states that have more lines almost completed
        res = (-gamestate.points  * len(gamestate.board) * len(gamestate.board[0])) + self.near_full_line(gamestate.board)
        return res
    
    def heuristic2(self, gamestate):
        # Gives more weight to the obtention of points.
        # The near_full_line function give more weight to states that have more lines almost completed
        res = (-gamestate.points  * len(gamestate.board) * len(gamestate.board[0])) + self.occupied_space(gamestate.board)
        return res
    
    def heuristic3(self, gamestate):
        #Equal weight to the completion of lines and points earned
        res = (-gamestate.points) + self.near_full_line(gamestate.board)
        return res
    
    def heuristic4(self, gamestate):
        #Equal weight for the number of pieces (how close if from gameover) and points earned
        res = (-gamestate.points) + len(gamestate.Q) + len(gamestate.L)
        return res
    