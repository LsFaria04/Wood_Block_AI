from PieceFactory import PieceFactory


def parse_config_file(filename):
   
   with open(filename, 'r') as file :
    board = []
    pieces = []
    points = 0
    current = ""
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
    

        if current == "b":
            board_line = list(map(lambda item: int(item), line.split(',')))
            board.append(board_line)
            
        elif current == "pi":

            if piece_counter == 3:
                #new piece row
                piece_counter = 0

            tile_size = 30
            offset_x, offset_y = 60, len(board) * tile_size + 70
            spacing = 180
            piece_conf = list(map(lambda item: int(item), line.split(',')))
            if len(piece_conf) != 4:
                print("Not a piece config")
            x, y = offset_x + piece_counter * spacing, offset_y
            piece = factory.create_piece(x,y, piece_conf[0], piece_conf[1], piece_conf[2], piece_conf[3])
            pieces.append(piece)
            piece_counter += 1

        elif current == "po":
            points = int(line)
    
    return (board, pieces, points)