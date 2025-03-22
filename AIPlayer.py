import numpy as np
from collections import deque
from Tree import TreeNode
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
            return self.bfs(gamestate)
        elif self.algorithm == 2:
            return self.dfs(gamestate)
        elif self.algorithm == 3:
            self.iterative_deepening()
        elif self.algorithm == 4:
            self.uniform_cost()
        elif self.algorithm == 5:
            return self.greedy(gamestate, self.heuristic3)
        elif self.algorithm == 6:
            return self.a_star(gamestate, self.heuristic3)
        elif self.algorithm == 7:
            #used the board plus the number of pieces as the weight in the algorithm, so that the heuristic weight is proportional to the size of the game 
            self.a_star_weighted(gamestate, self.heuristic3, (len(gamestate.board) + len(gamestate.Q) + len(gamestate.L)))
        else:
            print("Algorithm is not available")

    def bfs(self, gamestate):
        queue = deque([gamestate])          # initialize the queue to store the nodes
        visited = set()
        possibleGoalStates = []

        while queue:
            state = queue.popleft()
            visited.add(state) 
                                    # get first element in the queue
            if state.game_over():      # check goal state
                possibleGoalStates.append(state)

            for childState in state.children():
                if (childState not in visited):
                    queue.append(childState)
                    

        if possibleGoalStates:
            bestState = max([state for state in possibleGoalStates], key=lambda state: state.points)
            return bestState.move_history
        else:
            return None

    def dfs(self, gamestate):
        stack = [TreeNode(gamestate)]
        visited = set()

        while stack:
            node = stack.pop()
            if node.state.goal_state():
                return node
            
            if node.state not in visited:
                visited.add(node.state)

                for state in node.state.children():
                    new_node = TreeNode(state)
                    new_node.parent = node
                    stack.append(new_node)
        return None
    
    def iterative_deepening(self):
        return None
    
    def uniform_cost(self):
        states = []  # Min-heap for UCS
        heapq.heappush(states, (0, self.gamestate))
        visited = set()
        possibleGoalStates = []

        while states:
            cost, current_state = heapq.heappop(states)
            
            if current_state.game_over() :
                possibleGoalStates.append(current_state)
            
            visited.add(current_state)

            for childState in current_state.children():
                if current_state in visited:
                    continue
                heapq.heappush(states, (-childState.points + cost, childState))

        bestState = max([state for state in possibleGoalStates], key=lambda state: state.points)

        return bestState.move_history
    

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
        # Gives more weight to the obtention of points.
        # The near_full_line function give more weight to states that have more lines almost completed
        res = (-gamestate.points) + self.near_full_line(gamestate.board)
        return res
    
    