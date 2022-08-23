from Node import Node
#generate an empty board
row=[]
for i in range(3):
  row.append(-1)
board=[]
for i in range(3):
  board.append(row)

#some util function
def decide_win(piece_type, board):
  for i in range(3):
    true = 1
    for j in range(3):
      if board[i][j]!=piece_type:
        true=0
    if true == 1:
      return 1

  for j in range(3):
    true = 1
    for i in range(3):
      if board[i][j] != piece_type:
        true=0
    if true == 1:
      return 1
  
  if board[0][0] == piece_type and board[1][1] == piece_type and board[2][2] == piece_type:
    return 1
  if board[0][2] == piece_type and board[1][1] == piece_type and board[2][0] == piece_type:
    return 1
  
  return 0

def copy_board(board):
  new_board=[]
  for i in board:
    row=[]
    for j in i:
      row.append(j)
    new_board.append(row)

  
  return new_board


def place_pieces(piece_type,board):
  board_list=[]
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == -1:
        new_board= copy_board(board)
        new_board[i][j] = piece_type
        board_list.append(new_board)
  return board_list

#create root node
root_node=Node(0,board,-1)

#generate states
level = 0
prev_node_list=[]
prev_node_list.append(root_node)
master_list=[]
while level < 10:
  level = level+1
  level_list=[]
  for prev_node in prev_node_list:

    node_list=[]
    if level % 2 == 0:
      piece_type = 1
    else:
      piece_type = 0

    #find possible placement after this state
    if prev_node.win == 0:
      board_list=place_pieces(piece_type,prev_node.board)
    else:
      board_list = []
    
    #see_placement(board_list)


    for i in board_list:
      node = Node(level,i,prev_node)
      if decide_win(piece_type,i) == 1:
        if level % 2==0:
            node.set_win(-1)
        else:
            node.set_win(1)
      node_list.append(node)
      level_list.append(node)
    prev_node.set_next(node_list)

  #Move to next level
  prev_node_list=level_list
  #For ease of look up
  master_list.append(level_list)

#copy and edit a list
new_master_list=[]
for i in range(9):
  new_master_list.append([])
for i in range(9):
  for node in master_list[8-i]:
    if len(node.next)==0:
      node.set_utility(node.win)
    else:
      sum=0
      for n in node.next:
        sum=sum+n.utility

      node.set_utility(sum/3)
    new_master_list[8-i].append(node)
    
def make_move(node_list,piece_type):
  max=node_list[0].utility
  new_node = node_list[0]
  if piece_type==0:
      for n in node_list:
        if n.utility>max:
        #print(n.utility)
            max = n.utility
            new_node = n
  else:
      for n in node_list:
        if n.utility<max:
        #print(n.utility)
            max = n.utility
            new_node = n
  return new_node

def search_state(level,board, master_list):
  for node in master_list[level-1]:
    state=node
    true=1
    #print(state_board)
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j]!=state.board[i][j]:
          true=0
          
    if true == 1:
      return state
  
def view_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == -1:
                print("_",end=' ')
            elif board[i][j] == 1:
                print("X",end=' ')
            else:
                print("O",end=' ')
        print()
        
def game_over(board):
    for i in range(3):
        for j in range(3):
            if board[i][j]==-1:
                return 0
    else:
        return 1

#main program
player_piece_type = input("Choose the type: 0 goes first, 1 goes later.")
if int(player_piece_type) == 1:
    current_node_list = new_master_list[0]
    piece_type = 0
elif int(player_piece_type) == 0: 
    current_board = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
    piece_type = 1
    view_board(current_board)
    x=input("Please enter the x coordinate: (0-2)")
    y=input("Please enter the y coordinate: (0-2)")
    current_board[int(x)][int(y)]=0
    view_board(current_board)
    current_node_list = search_state(1,current_board,new_master_list).next
while True:

    print("Machine makes move: ")
    current_node = make_move(current_node_list,piece_type)
    current_board=current_node.board
    view_board(current_board)
    if game_over(current_board) == 1:
        print("It's a draw!")
        break
    if decide_win(piece_type,current_board)==1:
        print("Machine Wins!")
        break

    x=input("Please enter the x coordinate: (0-2)")
    y=input("Please enter the y coordinate: (0-2)")
    current_board[int(x)][int(y)]=int(player_piece_type)
    print("You make move: ")
    view_board(current_board)
    if game_over(current_board) == 1:
        print("It's a draw!")
        break
    if decide_win(int(player_piece_type),current_board)==1:
        print("Congratulations!")
        break
    
    #move to next level
    next_node=search_state(current_node.level+1,current_board,new_master_list)
    current_node_list=next_node.next
