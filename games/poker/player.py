import discord
from system import currencysystem as pineapple
class Player:
  def __init__(self, mention, client, message):
    self.mention = mention[2:-1]
    if self.mention[0] == '!':
      self.mention = self.mention[1:]
    self.client = client
    self.cards = []
    self.message = message
    self.bid = 0

  def give_card(self, card):
    self.cards.append(card)
  
  async def send_message(self):
    self.user = await self.client.fetch_user(self.mention)
    user = self.user
    self.name = user.name
    temp = ""
    cards = self.cards
    for i in range(len(cards) - 1):
      temp = temp + cards[i].to_string() + "  |  "

    temp += cards[len(cards) - 1].to_string() + " "

    embed=discord.Embed(title="Your Hand!", description=temp, color=0xEB459E)
    embed.set_author(name = f"{self.message.author.name}'s Game - {self.message.guild}", icon_url = self.message.author.avatar_url)

    await user.send(embed=embed)

  def raise_bid(self, amount):
    self.bid += amount
    pineapple.spend_currency(self.user, self.message.guild, amount)
    
  def to_string(self):
    return f'<@{self.mention}> - {str(self.bid)} pineapple'

  def show_hand(self):
    str = []
    for card in self.cards:
      str.append(card.to_string())
    return "  |  ".join(str)