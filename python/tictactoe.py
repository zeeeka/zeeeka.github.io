board =         [
            ['X', 'X', 'X', ' '],
            ['X', 'X', ' ', ' '],
            ['X', ' ', 'O', 'X'],
            [' ', ' ', 'O', 'X']
        ]  

def row_winner (board) :
    for row in board:
        for _ in range(len(row)) :
            if row[_] == row[_-1] and row[_]!=' ' :
                winner = True
            else : 
                winner = False
                break
        if winner : 
            break
    return winner

def column_winner (board) :
    for i in range(len(board)):
        for _ in range(len(board[0])):
            if board[_][i] == board[_-1][i] and board [_][i] != ' ' :
                winner = True
            else :
                winner = False 
                break
        if winner :
            break
    return winner

def diagonal_winner(board):
    one = []
    two = []
    for row in range(len(board)) :
        for i in range(len(board[0])) :
            if row == i :
                one.append(board[row][i])
            elif row + i == len(board[0])-1:
                two.append(board[row][i])
    if len(set(one)) ==1 and ' ' not in set(one) :
        winner = True
    elif len(set(two)) == 1 and ' ' not in set(two) :
        winner = True
    else : 
        winner=False
    return winner

def winner (board) :
    if row_winner(board) or column_winner(board) or diagonal_winner(board) :
        return True
    else :
        return False

assert_equal(
    winner(
        [
            ['X', 'X', 'X', ' '],
            ['X', 'X', ' ', ' '],
            ['X', ' ', 'O', 'X'],
            [' ', ' ', 'O', 'X']
        ]
    ),
    False
)
assert_equal(
    winner(
        [
            ['X', ' ', 'X'],
            ['O', 'X', 'O'],
            ['O', 'O', 'O']
        ]
    ),
    True
)
assert_equal(
    winner(
        [
            ['X', ' '],
            ['X', 'O']
        ]
    ),
    True
)

            
