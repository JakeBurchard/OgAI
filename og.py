from copy import deepcopy
TRANSPOSITION_TABLE = {}
Empty = '-'
Player_X = 'x'
Player_O = 'o'
INFINITY = 999999999
EXPLORED = 0
def add_transposition(board, utility):
    if ''.join(board) not in TRANSPOSITION_TABLE:
        TRANSPOSITION_TABLE[''.join(board)] = utility
    
    boards = []
    symmetries = [
    [12,8,4,0,13,9,5,1,14,10,6,2,15,11,7,3],
    [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
    [3,7,11,15,2,6,10,14,1,5,9,13,0,4,8,12],
    [3,2,1,0,7,6,5,4,11,10,9,8,15,14,13,12],
    [12,13,14,15,8,9,10,11,4,5,6,7,0,1,2,3],
    [15,11,7,3,14,10,6,2,13,9,5,1,12,8,4,0],
    [3,7,11,15,2,6,10,14,1,5,9,13,0,4,8,12],
    [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
    ]
    
    #populate list of all symmetrical boards
    for sym in symmetries:
        tmp = [0]*16
        for i in range(16):
            tmp[i] = board[sym[i]]
        boards.append(tmp)
        
    #add each symmetrical board to the transposition table
    for x in boards:
        if ''.join(x) not in TRANSPOSITION_TABLE:
            TRANSPOSITION_TABLE[''.join(x)] = utility

def in_table(board):
    if ''.join(board) in TRANSPOSITION_TABLE:
        return TRANSPOSITION_TABLE[''.join(board)]
    else:
        return False
    

def max_value(test_game, player):
    global EXPLORED
    #check if the board is full
    win = test_game.winner()
    if win != False:
        if win == Player_X:
            return -1
        elif win == Player_O:
            return 1
        elif win == 3:
            return 0
            
    v = -INFINITY
    
    #switch the player
    if player == Player_X:
        player = Player_O
    else:
        player = Player_X
    for s in test_game.successors():
        EXPLORED += 1
        #expand trees for all legal moves
        new_test = OgGame()
        new_test.board = test_game.board[:]
        new_test.make_move(s, player)
        
        #check of the current state is in the transposition table
        #if so, look up its utility and assign it
        trans = in_table(new_test.board)
        if trans: 
            v = trans
        else:
            #if not in the table, continue down the tree
            v = max(v, min_value(new_test, player))
        add_transposition(new_test.board, v)
    return v
def min_value(test_game, player):
    global EXPLORED
    #check if the board is full
    win = test_game.winner()
    if win != False:
        if win == Player_X:
            return -1
        elif win == Player_O:
            return 1
        elif win == 3:
            return 0
    v = INFINITY
    
    #switch the player
    if player == Player_X:
        player = Player_O
    else:
        player = Player_X
    for s in test_game.successors():
        EXPLORED += 1
        #expand trees for all legal moves
        new_test = OgGame()
        new_test.board = test_game.board[:]
        new_test.make_move(s, player)
        
        #check of the current state is in the transposition table
        #if so, look up its utility and assign it
        trans = in_table(new_test.board)
        if trans: 
            v = trans
        else:
            #if not in the table, continue down the tree    
            v = min(v, max_value(new_test, player))
        add_transposition(new_test.board, v)
    return v
def minimax_decision(game,player): 
    global EXPLORED
    args = {}
    legal_moves = game.successors()
    
    #find the utility of every legal move
    for move in legal_moves:
        EXPLORED += 1
        test_game = OgGame()
        test_game.board = game.board[:]
        test_game.make_move(move, player) 
        if player == Player_X:
            move_utility = max_value(test_game, player)
        else:
            move_utility = min_value(test_game, player)
        args[move] = move_utility
        
        #add the utility and board state to the transposition table
        add_transposition(test_game.board, move_utility)
        
    #determine whether to return the max or min of the utilities depending on player
    if player == Player_X:
        return min(args.iterkeys(), key=lambda k: args[k])
    else:
        return max(args.iterkeys(), key=lambda k: args[k])
    

def max_value_ab(test_game, player, alpha, beta):
    global EXPLORED
    #check if the board is full
    win = test_game.winner()
    if win != False:
        if win == Player_X:
            return -1
        elif win == Player_O:
            return 1
        elif win == 3:
            return 0
            
    v = -INFINITY
    
    #switch the player
    if player == Player_X:
        player = Player_O
    else:
        player = Player_X
    for s in test_game.successors():
        EXPLORED += 1
        #expand trees for all legal moves
        new_test = OgGame()
        new_test.board = test_game.board[:]
        new_test.make_move(s, player)
        
        #check of the current state is in the transposition table
        #if so, look up its utility and assign it
        trans = in_table(new_test.board)
        if trans: 
            v = trans
        else:
            #if not in the table, continue down the tree  
            v = max(v, min_value_ab(new_test, player, alpha, beta))
        
        #check the utility against the current beta value
        if v >= beta:
            return v
        alpha = max(alpha, v)
        add_transposition(new_test.board, v)
    return v
def min_value_ab(test_game, player, alpha, beta):
    global EXPLORED
    #check if the board is full
    win = test_game.winner()
    if win != False:
        if win == Player_X:
            return -1
        elif win == Player_O:
            return 1
        elif win == 3:
            return 0
    v = INFINITY
    
    #switch the player
    if player == Player_X:
        player = Player_O
    else:
        player = Player_X
    for s in test_game.successors():
        EXPLORED += 1
        #expand trees for all legal moves
        new_test = OgGame()
        new_test.board = test_game.board[:]
        new_test.make_move(s, player)
        
        #check of the current state is in the transposition table
        #if so, look up its utility and assign it
        trans = in_table(new_test.board)
        if trans: 
            v = trans
        else:
            #if not in the table, continue down the tree 
            v = min(v, max_value_ab(new_test, player, alpha, beta))
            
        #check the utility against the current alpha value
        if v <= alpha:
            return v
        beta = min(beta, v)
        add_transposition(new_test.board, v)
    return v 
def ab_pruning(game, player):  
    global EXPLORED
    args = {}
    legal_moves = game.successors()
    
    #find the utility of every legal move
    for move in legal_moves:
        EXPLORED += 1
        test_game = OgGame()
        test_game.board = game.board[:]
        test_game.make_move(move, player)
        if player == Player_X:
            move_utility = max_value_ab(test_game, player, -INFINITY, INFINITY)
        else:
            move_utility = min_value_ab(test_game, player, -INFINITY, INFINITY)
        
        args[move] = move_utility
        
        #add the utility and board state to the transposition table
        add_transposition(test_game.board, move_utility)
        
    #determine whether to return the max or min of the utilities depending on player
    if player == Player_X:
        return min(args.iterkeys(), key=lambda k: args[k])
    else:
        return max(args.iterkeys(), key=lambda k: args[k])
    
class OgGame:
    def __init__(self):
        #self.board = ['-']*16
        self.board = ['-', '-', '-', '-', '-', 'x', '-', '-', '-', '-', 'x', 'o', '-', '-', '-', 'o']
       
    def display(self):
        for line in [self.board[0:4], self.board[4:8], 
                    self.board[8:12], self.board[12:16]]:
            print ' '.join(line)
    
    #return list of legal moves based on current board
    def successors(self):
        return [pos for pos in range(16) if self.board[pos] == Empty]
        
        
    def extra_turn(self, legal_moves, player):
        for cell in legal_moves:
            #for every cell in the board, populate list of adjacent cells
            if cell in [4,8,12]:
                new_cells = [x for x in [cell - 4, cell + 4, cell + 1] if x in range(16)]
            elif cell in [3,7,11]:
                new_cells = [x for x in [cell - 4, cell + 4, cell - 1] if x in range(16)]
            else:
                new_cells = [x for x in [cell - 4, cell + 4, cell - 1, cell + 1] if x in range(16)]
            adj_count = 0
            
            #check if adjacent cells are the player's own
            for new_cell in new_cells:
                if self.board[new_cell] == player:
                    adj_count += 1
                    
            #if all adjacent cells are own player's, return the cell
            if adj_count == len(new_cells):
                return cell
        return -1
                
    def make_move(self, move, player, true_human = False):
        self.board[move] = player
        legal_moves = self.successors()
        
        #check if a move results in a fully inclosed space
        new_move = self.extra_turn(legal_moves, player)
        if new_move != -1:
            #take the extra space
            self.make_move(new_move, player, true_human)
            
            #get an extra turn
            if true_human == True:
                human(self, player)
            else:
                computer(self, player)
    def winner(self):
        if not self.successors():
            max_vals = max(set(self.board), key=self.board.count)
            min_vals = min(set(self.board), key=self.board.count)
            if max_vals != min_vals:
                return max_vals
                
            #tie game
            else:
                return 3
        else:
            return False
        

        
def human(game, player):
    if not game.winner():
        legal_moves = game.successors()
        print 'Player "%s" turn' % player
        print "legal moves: " + str(legal_moves)
        move = int(raw_input("Move:"))
        while move not in legal_moves:
            print "'%s' is not a legal move" % move
            print "legal moves: " + str(legal_moves)
            move = int(raw_input("Move:"))
        game.make_move(move, player, True)

    

def computer(game, player):
    if not game.winner():
        move = ab_pruning(game, player)
        game.make_move(move, player)


def play_game():
    global EXPLORED
    game = OgGame()
    print """-------
  OG 
-------"""
    print """Pick an option
    1) Human vs. Human
    2) Human vs. Computer
    3) Computer vs. Computer
    """
    choice = int(raw_input("Choice:"))
    while choice not in [1,2,3]:
        print "'%s' is not a valid choice" % move
        choice = int(raw_input("Choice:"))
    while True:
        #player O
        if game.winner(): 
            break
        game.display()
        if choice in [1,2]:
            human(game, Player_O)
        else:
            computer(game, Player_O)
            print "Number of states explored: " + str(EXPLORED)
            EXPLORED = 0
        print "--------------"    
        #player X    
        if game.winner(): 
            break
        game.display()
        if choice in [2,3]:
            computer(game, Player_X)
            print "Number of states explored: " + str(EXPLORED)
            EXPLORED = 0

        else:
            human(game, Player_X)
        print "--------------"
    print "--------------"
    game.display()       
    if game.winner() != 3:
        print 'Player "%s" wins' % game.winner()
    else:
        print 'The game is a tie'

if __name__ == "__main__":
    play_game()
