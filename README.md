# Wood Block - IA First Project

## Game Presentation

"World Block Puzzle" is a captivating and challenging single-player game that combines elements of strategy, spatial reasoning, and pattern recognition. The objective of the game is to fit different block shapes into a given grid, filling the lines/columns of the grid without leaving any gaps.

- **Game Board:** The game board consists of a rectangular grid with varying dimensions (e.g., 5x5, 10x10).

- **Blocks:** The game includes a set of blocks of different shapes and sizes. Each block is a combination of smaller square units arranged in various patterns.

- **Objective:** The player must place all blocks on the grid in such a way that every square in a line or column are filled. The game is won when all the pieces are played.

- **Scoring:** The player's score is determined by the time taken to complete the puzzle, lines/columns filled, with n points awarded per block. Bonus points are awarded when several lines/columns are filled at the same time.

## Search Problem Formulation

- **States:**
     - **Board Matrix:** B[N,M] filled with 0 or 1. 0 represents empty square and 1 represents occupied.

     - **Current Selection of pieces:** S[3], represents the pieces that can be played

     - **Queue with the next pieces:** queue Q with all the other pieces.

- **Initial State:**
    - B[N,M] = {0}, empty matrix
    - S = [P1, P2, P3], where P1,P2 and P3 are the first 3 pieces.
    - Q = {P4, P5, P6, ...}

- **Goal State:**
    - B[N,M] = _, it can have pieces
    - S = [], Q = {}, all the pieces were played

- **Operators:**
    - **Name:** Move(Piece, Position)
    - **Preconditions:** The board must have space for the piece in the position selected
    - **Effects:** Piece added to the board, removed from the current selection list and a new piece is popped from the queue and inserted into the selection list.
    - **Cost:** Moves that bring more lines/columns closer to completion have a higher cost.
    Moves that complete lines/columns have a very high cost.
    The player should choose the move with the highest cost.

- **Heuristic and evaluation functions:**
    - **Closer to complete:** Evaluates the piece/move by the improvement it gives to a line/column completion

    - **Shape evaluation:**
    Evaluates the shape of the piece and gives a higher score if the position has the perfect shape for that piece

## Bibliography
https://play.google.com/store/apps/details?id=com.block.puzzle.free.wood&hl=en 


