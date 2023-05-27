class Hand:
  def __init__(self):
    self.cards = []

  def add_card(self, card):
    self.cards.append(card)

  def clear(self):
    self.cards = []

  def get_value(self):
    value = 0
    aces = 0
    for card2 in self.cards:
      if card2.get_rank() == 1:
        if self.is_soft() and aces == 0:
          value += 11
          aces += 1
        else:
          value += 1

      else:
        if card2.rank >= 10:
          value += 10
        else:
          value += card2.rank
    
    return value

  def is_blackjack(self):
    cards = self.cards
    if len(cards) != 2: 
      return False
    else:
      ace = False
      faceCard = False
      for i in range(len(cards)):
        temp =  cards[i].rank
        if temp == 1:
          ace = True
        if temp >= 10:
          faceCard = True

      return ace and faceCard

  def is_soft(self):
    cards = self.cards
    value = 0
    aces = 0
    for card in cards:
      if card.rank == 1:
        aces += 1
      else:
        value += card.rank

    if aces != 0:
      if len(cards) == 2 and (aces == 2):
        return True
      elif aces == 1:
        if (value + 11) <= 21:
          return True
        else: 
          return False
      else:
        if (value + 11) <= (21 - (aces - 1)):
          return True
        else:
          return False
    return False

  def show_cards(self):
    cards = self.cards
    for card in cards:
      card.faceUp = True
    return self

  def compare_to(self, otherHand):
    thisValue = self.get_value()
    otherValue = otherHand.get_value()

    if self.is_blackjack() and otherHand.is_blackjack():
      return 0
    elif thisValue == otherValue:
      return 0
    elif thisValue > otherValue:
      return 1
    elif thisValue < otherValue:
      return -1
    else:
      return 0

  def to_string(self):
    temp = ""
    cards = self.cards
    for i in range(len(cards) - 1):
      temp = temp + cards[i].to_string() + "\n"

    temp += cards[len(cards) - 1].to_string() + " "

    return temp