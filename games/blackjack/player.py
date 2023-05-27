from games.blackjack.hand import Hand
class Player:
  def __init__(self, name = "Default"):
    self.name = name
    self.hand = Hand()

  def give_card(self, card):
    self.hand.add_card(card)

  def has_blackjack(self):
    return self.hand.is_blackjack()

  def has_bust(self):
    return self.hand.get_value() > 21

  def show_hand(self):
    return self.hand

  def hand_value(self):
    return self.hand.get_value()  