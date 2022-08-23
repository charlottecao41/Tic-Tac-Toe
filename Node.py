class Node:
  def __init__(self,level,board, prev_node):
    self.level=level
    self.board=board
    self.prev = prev_node
    self.next=[]
    self.utility=0
    self.win=0

  def set_next(self,node_list):
    self.next = node_list

  def set_prev(self,node):
    self.prev=node
  
  def set_board(self,board):
    self.board=board
  
  def set_level(self,level):
    self.level=level

  def set_utility(self,utility):
    self.utility=utility
  
  def set_win(self,win):
    self.win=win