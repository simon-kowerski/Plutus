from games.blackjack.player import Player
from games.cards import Deck

win_exp = 5
win_currency = 29

import discord
games = []
#determines whether or not continuing game or starting a new one
async def handle_input(message, client): 
  gameExist = False
  for game in games:
    if game.author is message.author and game.channel is message.channel:        
      if "new" in message.content:
        gameExist = False
        game.end_game()
      else:
        await game.turn_manager(message)
        gameExist = True

  if not gameExist:
    main = await message.channel.send(message.author.mention + " has started playing blackjack.")
    games.append(BlackJack())
    await games[-1].blackjack_main(message, client, main)
    
class BlackJack:
  #sets up and starts game
  async def blackjack_main(self, message, client, main):
    self.channel = message.channel
    self.author = message.author
    self.client = client
    self.mainMessage = main
    self.turnKeepGoing = True
    self.deck = Deck()
    self.deck.shuffle()
    
    self.player = Player(name = self.author.name)
    self.player.give_card(self.deck.take_card())
    self.player.give_card(self.deck.take_card())

    self.dealer = Player(name = "Dealer")
    self.dealer.give_card(self.deck.take_card())
    self.dealer.give_card(self.deck.take_card())

    embed=discord.Embed(description = "...", color=0xEB459E)
    self.message = await self.channel.send(embed=embed)
    
    await self.beforeTurnOutput()

  #outputs prompt for user to start turn
  async def beforeTurnOutput(self, send=False):
    channel = self.channel
    player = self.player
    tempHand = player.show_hand()    

    if(player.show_hand().is_soft()):
      score = "Soft " + str(player.hand_value())
    else:
      score = str(player.hand_value())

    output = self.author.mention + "'s Hand - " + score + "\n" + tempHand.to_string()	

    if(player.has_blackjack()):
      output += "\nYou have Blackjack!"
   
    if send:
      self.mainMessage = await channel.send(self.author.mention + " is continuing blackjack.")
      self.message = await channel.send(embed=self.generate_embed(output, True))
    await self.message.edit(embed=self.generate_embed(output, True))

  #user turn
  async def turn(self, move):
    player = self.player
    deck = self.deck
    
    if (move == "hit"):
      player.give_card(deck.take_card())
    
    if (move == "stand"):
      self.turnKeepGoing = False

    if(player.hand_value() > 21):
      self.turnKeepGoing = False

    if self.turnKeepGoing:
      await self.beforeTurnOutput()
    else: 
      await self.dealer_turn()
      self.end_game()

    self.player = player
    self.deck = deck

  #after user stands or bust, dealer turn
  async def dealer_turn(self):
    player = self.player
    deck = self.deck
    dealer = self.dealer
    tempHand = dealer.show_hand()
    win = False
    output = self.author.mention + "'s Hand - " + str(player.hand_value()) + "\n" + player.show_hand().to_string() + "\n\n"
    if dealer.has_blackjack():
      output += self.client.user.mention + "'s hand - " + str(dealer.hand_value()) + "\n" + tempHand.to_string() + "\n"
      output += "The dealer has Blackjack!\n"

      if player.has_blackjack():
        output += self.author.mention + " has Blackjack and has tied with the dealer!"
      else:
        output += self.author.mention + " has lost to the dealer with " + str(player.show_hand().get_value())

    else:
      while (dealer.hand_value() == 17 and dealer.show_hand().is_soft()) or dealer.hand_value() < 17:
        dealer.give_card(deck.take_card())
      
      output += self.client.user.mention + "'s hand - " + str(dealer.hand_value()) + "\n" + tempHand.to_string() + "\n"
      tempHand = dealer.show_hand()
      output += "\nThe dealer has " + str(dealer.hand_value()) + "\n"
      if player.has_blackjack():
        output += self.author.mention + " has Blackjack and has beat the dealer!"
        win = True
      elif player.hand_value() > 21:
        output += self.author.mention + " has lost to the dealer with " + str(player.hand_value())
      else:
        if dealer.hand_value() > 21:
          output += "The dealer has bust!\n"
          output += self.author.mention + " has beat the dealer with " + str(player.hand_value())
          win = True
        else:
          dealerVal = dealer.hand_value()
          playerVal = player.hand_value()
          if dealerVal > playerVal:
            output += self.author.mention + " has lost to the dealer with " + str(player.hand_value())
          elif dealerVal == playerVal:
            output += self.author.mention + " has tied with the dealer"
          else:
            output += self.author.mention + " has beat the dealer with " + str(player.hand_value())
            win = True
        
    await self.message.edit(embed = self.generate_embed(output, False))
    if win:
      from system import levelsystem, currencysystem
      await levelsystem.add_exp(self.author, self.channel.guild, win_exp, channel = self.channel)
      win_amount = win_currency
      if player.has_blackjack():
        win_amount = 83
      await currencysystem.add_currency(self.author, self.channel.guild, win_amount)
    await self.mainMessage.delete()

  #ends game, and removes it from list 
  def end_game(self):
    position = 0
    for game in games:
      if game.author == self.author:
        if game.channel == self.channel:
          games.pop(position)
          return 0
      position += 1

  #starts user turn or prompts for new input
  async def turn_manager(self, message):
    move = message.content.split(" ")
    length = len(move)
    move.pop(0)

    if length == 1:
      await self.beforeTurnOutput(send=True)
    elif (move[0] != "hit" and move[0] != "stand"):
      await self.channel.send("Invalid input, do you want to hit or stand?")
    else:
      await self.turn(move[0])
    await message.delete()

  def generate_embed(self, output_text, player_turn):
    embed=discord.Embed(description = output_text, color=0xEB459E)
    embed.set_author(name=self.author.display_name + "'s Blackjack", icon_url=self.author.avatar_url)
    if player_turn:
      embed.set_footer(text="&blackjack hit  |  &blackjack stand  |  &blackjack new")
    else:
      embed.set_footer(text="Game Over!  |  &blackjack new")
    return embed
    