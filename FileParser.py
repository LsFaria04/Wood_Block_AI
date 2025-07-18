from PieceFactory import PieceFactory
from datetime import datetime
import ast


def parse_config_file(filename):
   '''
   Parses the file with the name given as argument and returns the game configuration stored in the file
   '''
   
   with open(filename, 'r') as file :
    board = []
    pieces = []
    points = 0
    current = ""
    ai = ""
    moves = []
    factory = PieceFactory()
    piece_counter = 0
    for line in file:
      
      #check if the line is a section separator
        if line == "board\n":
            current = "b"
            continue
        elif line == "pieces\n":
            current = "pi"
            continue
        elif line == "points\n":
            current = "po"
            continue
        elif line == "ai\n":
            current = "ai"
        elif line == "moves\n":
            current = "mov"
    
        if current == "b":
            board_line = list(map(lambda item: int(item), line.split(',')))
            board.append(board_line)
            
        elif current == "pi":

            if piece_counter == 3:
                #new piece row
                piece_counter = 0

            tile_size = 30
            screen_width = 600 / tile_size
            screen_height = 720 / tile_size

            offset_x = 60 
            offset_y = ((screen_height - len(board)) // 2 + len(board)) * tile_size + 50
            spacing = 180

            piece_conf = list(map(lambda item: int(item), line.split(',')))
            if len(piece_conf) != 4:
                print("Not a piece config!!!")
                piece_counter += 1
                continue
            x, y = offset_x + piece_counter * spacing, offset_y
            piece = factory.create_piece(x,y, piece_conf[0], piece_conf[1], piece_conf[2], piece_conf[3])
            pieces.append(piece)
            piece_counter += 1

        elif current == "po":
            points = int(line)
        elif current == "ai":
            ai = line
        elif current == "mov" and line.strip() != 'moves':
            try:
                moves.append(ast.literal_eval(line.strip()))  # Convert string to actual Python data structure
            except Exception as e:
                print(f"Error parsing move: {line.strip()}, {e}")
    
    return (board, pieces, points, ai, moves)

def store_results(algorithm, heuristic, move_history, time_execution, points, memory_used):
    '''
    Stores the results of a game solved by the AI.
    '''
    now = datetime.now()
    # Format the date and time
    formatted_date = now.strftime("%Y_%m_%d %H_%M_%S")

    with open("saved_ai_results/" + str(formatted_date) + ".txt", "w") as file:

        file.write("Saved at : " + formatted_date + "\n\n")
        file.write("Algorithm: " + algorithm + "\n")
        if algorithm in ["Greedy", "A*", "A* Weighted", "greed", "astar", "astarw"]:
            file.write("Heuristic: " + heuristic + "\n")
        file.write("Execution Time: " + str(time_execution) + "\n")
        file.write("Points: " + points + "\n")
        file.write("Memory Used: " + memory_used + "\n")
        file.write("Move History: \n\n")

        for state in move_history:
            file.write("Move Made (piece index, cords): ")
            file.write(str(state.move_made[1]) + ", " + str(state.move_made[2]) + "\n")
            for line in state.board:
                for element in line:
                    file.write(str(int(element)))
                file.write("\n")
            file.write("\n")
            
            
