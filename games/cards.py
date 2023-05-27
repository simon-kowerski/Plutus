class Deck:
  cards = []

  def __init__(self):
    for suit in range(1, 5):
      for rank in range(1, 14):
	      self.cards.append(Card(rank, suit))

  def shuffle(self):
    import random
    random.shuffle(self.cards)

  def take_card(self):
    if not self.cards:
      return None
    else:
      return self.cards.pop(0)

class Card:
  rank = 1
  suit = 4
  
  def __init__(self, rank, suit):
    if rank == 1:
      rank = 14
    self.rank = rank
    self.suit = suit
    self.faceUp = True

  def get_rank(self):
    return self.rank
  
  def to_string(self):
    if not self.faceUp:
      return "[Face Down]"
      
    retsuit = " :spades:"
    if self.suit == 1:
      retsuit = " :clubs:"
    elif self.suit == 2:
      retsuit = " :diamonds:"
    elif self.suit == 3:
      retsuit = " :hearts:"

    retrank = "Ace"
    if self.rank == 11:
      retrank = "Jack"
    elif self.rank == 12:
      retrank = "Queen"
    elif self.rank == 13:
      retrank = "King"
    elif self.rank != 14:
      retrank = str(self.rank) 

    return retrank + retsuit

  def __eq__(self, other_place):
    if self.suit == other_place.suit:
      return True
    else:
      return False
    
  def __gt__(self, other_place):
    if self.suit > other_place.suit:
      return True
    else:
      return False
        
  def __ge__(self, other_place):
    if self.suit >= other_place.suit:
      return True
    else:
      return False
    
  def __lt__(self, other_place):
    if self.suit < other_place.suit:
      return True
    else:
      return False
        
  def __le__(self, other_place):
    if self.suit <= other_place.suit:
      return True
    else:
      return False

