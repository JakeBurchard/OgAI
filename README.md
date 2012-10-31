OgAI
====

AI for playing a simple game called Og using the minimax algorithm with alpha-beta pruning, transposition table, and board symmetries.
There are options for human vs. human, human vs. AI, and AI vs. AI play.

Rules
====

Two players start with an empty 4x4 board and take turns placing marbles in the grid cells with the objective being to control
the most cells by the end of the game. If a cell is completely surrounded on all sides by a single players marbles (or only on 2 or 3
sides in the case of a corner or edge cell), that player may place a marble in the surrounded cell and take another turn. Play continues
until all cells are filled.

