from games.cards import Deck
from games.poker.player import Player
from system import currencysystem as currency
import discord
win_exp = 25

#get rid of being able to play by yourself or someone else twice 

games = []
#determines whether or not continuing game or starting a new one
async def handle_input(client, reaction = None, user = None, message = None): 
  if message:
    for game in games:
      if game.author is message.author and game.channel is message.channel: 
        if "@" in message.content:
          await game.channel.send("Ending previously started game")
          await game.end_game()
          await game.channel.send("Starting new game")
          
    main = await message.channel.send(message.author.mention + " has started a game of Poker.")
    games.append(Poker())
    await games[-1].poker_main(message, client, main)
      
  if reaction:
    for game in games:
      if reaction.message == game.message: 
        await game.turn_manager(reaction, user)
    
class Poker: #texas holdem
  async def poker_main(self, message, client, main):
    self.channel = message.channel
    self.author = message.author
    self.client = client
    self.mainMessage = main
    self.turnKeepGoing = True
    self.deck = Deck()
    self.deck.shuffle()

    self.bid_order = []

    embed=discord.Embed(description = "...", color=0xEB459E)
    self.message = await self.channel.send(embed=embed)
    
    mentions = message.content.split(" ") 
    mentions.pop(0)
    mentions.append(self.author.mention)
    if len(mentions) <= 1:
      await self.channel.send("Ha, no friends...\nGo mention more people.")
      await self.channel.send("https://tenor.com/view/smile-person-akirambow-alone-sad-gif-26359091")
      await self.end_game()
      return 
      
    players = []
    for mention in mentions:
      player = players.append(Player(mention, client, message))

    playerpos = 0
    removeplayers = []
    for player in players:
      if currency.get_currency(await self.client.fetch_user(player.mention), self.channel.guild) < 50:
        removeplayers.append(playerpos)
        await self.channel.send(f"<@{player.mention}> doesn't have enough Pineapple to play. Be less broke and come back later.")
      else:
        player.give_card(self.deck.take_card())
        player.give_card(self.deck.take_card())
        await player.send_message()
        playerpos += 1

    for i in removeplayers:
      players.pop(i)

    if len(players) <= 1:
      await self.channel.send("You no longer have enough players to start a game. Go get richer friends and come back.")
      await self.end_game()
      return
    
    self.players = players
    self.dealer = []
    self.dealer_cards = []
    for i in range(3):
      self.dealer_cards.append(self.deck.take_card())
      self.dealer.append(self.dealer_cards[-1].to_string())

    self.footers = [ # offset by 1 because of raise
      'Raise by 10, 20, 30, 40, or 50 Pineapple',
      'small - 10 pineapple  |  large - 20 pineapple',
      'match initial bid | fold',
      'raise highest | match highest | fold'
    ]

    self.curr_turn = 0
    self.match = 0
    self.table_total = 0
    
    self.add_to_bid_order()
    current = self.bid_order[0]
    game_message = f'<@{current.mention}> place your initial bid'  
    footer = self.footers[1]
    await self.generate_embed(game_message, footer, hide = True)
    await self.message.add_reaction("🇸")
    await self.message.add_reaction("🇱")

  async def turn_manager(self, reaction, reaction_user):
    current = self.bid_order[0]
    await reaction.remove(reaction_user)
    if reaction_user.mention != f'<@{current.mention}>' and reaction_user.mention != f'<@!{current.mention}>':
      return

    if self.curr_turn <= 1: #initial round of bidding
      await self.initial_bids(reaction)

    if self.curr_turn == 2 or self.curr_turn == 3:
      await self.flop(reaction)
      
    if len(self.players) <= 1:
      await self.end_game()

    if self.curr_turn == 4:
      await self.end_game()
    
  async def initial_bids(self, reaction):
    current = self.bid_order[0]
    if self.curr_turn == 0: #very first player
      self.curr_turn = self.curr_turn + 1
      if reaction.emoji == "🇱":
        current.raise_bid(20)
        self.match = 20
        self.table_total += 20
      if reaction.emoji == "🇸":
        current.raise_bid(10)
        self.match = 10
        self.table_total += 10
      await self.message.clear_reactions()
      
      current = self.bid_order[1]
      game_message = f'<@{current.mention}> place your initial bid'
      await self.generate_embed(game_message, self.footers[self.curr_turn + 1], hide = True)
      
      await self.message.add_reaction("🇲")
      await self.message.add_reaction("🇫")
    
    else: #matching first player or folding
      if reaction.emoji == "🇲":
        current.raise_bid(self.match)
        self.table_total += self.match
      if reaction.emoji == "🇫":
        self.players.remove(current)
      current = self.bid_order[0]
      game_message = f'<@{current.mention}> place your initial bid'
      await self.generate_embed(game_message, self.footers[self.curr_turn + 1], hide = True)

    if len(self.bid_order) == 1:
      self.curr_turn = self.curr_turn + 1
      await self.message.clear_reactions()

    self.bid_order.pop(0)

  async def flop(self, reaction):
    if(len(self.bid_order) == 0):
      self.add_to_bid_order()
    current = self.bid_order[0]
    
    if self.curr_turn == 2:
      await self.f_m_r_reactions_message(current)
      self.curr_turn += 1
      return

    else:
      if reaction.emoji == "🇫":
        self.players.remove(current)
      if reaction.emoji == "🇲":
        previous = current.bid
        raise_amount = self.match - previous
        current.raise_bid(raise_amount)
        self.table_total += raise_amount
      if reaction.emoji == "🇷":
        await self.raise_(current)
        return

      if reaction.emoji == "1️⃣":
        raise_amount = 10 + self.match - current.bid
        current.raise_bid(raise_amount)
        self.table_total += raise_amount
        self.match = current.bid
      if reaction.emoji == "2️⃣":
        raise_amount = 20 + self.match - current.bid
        current.raise_bid(raise_amount)
        self.table_total += raise_amount
        self.match = current.bid
      if reaction.emoji == "3️⃣":
        raise_amount = 30 + self.match - current.bid
        current.raise_bid(raise_amount)
        self.table_total += raise_amount
        self.match = current.bid
      if reaction.emoji == "4️⃣":
        raise_amount = 40 + self.match - current.bid
        current.raise_bid(raise_amount)
        self.table_total += raise_amount
        self.match = current.bid
      if reaction.emoji == "5️⃣":
        raise_amount = 50 + self.match - current.bid
        current.raise_bid(raise_amount)
        self.table_total += raise_amount
        self.match = current.bid

      self.bid_order.pop(0)
      if len(self.bid_order) != 0:
        current = self.bid_order[0]
        await self.f_m_r_reactions_message(current)
      else:
        if len(self.dealer) == 5:
          self.curr_turn = self.curr_turn +1
        else:
          self.dealer.append(self.deck.take_card().to_string())
          self.add_to_bid_order()
          self.curr_turn = self.curr_turn - 1
          await self.flop(reaction)
  
  async def f_m_r_reactions_message(self, current):
    game_message = f'<@{current.mention}> would you like to match {self.match} pineapple, raise, or fold?'
    await self.generate_embed(game_message, self.footers[3])
    await self.message.clear_reactions()
    await self.message.add_reaction("🇷")
    await self.message.add_reaction("🇲")
    await self.message.add_reaction("🇫")
  
  async def raise_(self, current):
    game_message = f'<@{current.mention}> how much would you like to raise by?'
    await self.generate_embed(game_message, self.footers[0])
    await self.message.clear_reactions()
    await self.message.add_reaction("1️⃣")
    await self.message.add_reaction("2️⃣")
    await self.message.add_reaction("3️⃣")
    await self.message.add_reaction("4️⃣")      
    await self.message.add_reaction("5️⃣")
    self.add_to_bid_order(current)

  def add_to_bid_order(self, start = None):
    if start:
      for pos in range(len(self.players)):
        if self.players[pos] is start:
          break

      very_first = self.bid_order[0]
      self.bid_order.clear()
      front = self.players[pos+1:]
      back = self.players[:pos]
      self.bid_order.append(very_first)
      for player in front:
        self.bid_order.append(player)
      for player in back:
        self.bid_order.append(player)
    else:
      for player in self.players:
        self.bid_order.append(player)
  
  async def generate_embed(self, game_message, footer, hide = False, edit = True, end = False):
    embed = discord.Embed(color=0xEB459E)
    embed.set_author(name = f"{self.author.name}'s game of Poker", icon_url = self.author.avatar_url)
    embed.set_footer(text=footer)
    
    players = ''
    for i in self.players:
      players += i.to_string()
      if end:
        players += " - " + i.show_hand()
      players += "\n"
    
    players[:-1]
    embed.add_field(name = f'Player Bids - {self.table_total} pineapple', value = players)

    if not hide:
      table = "  |  ".join(self.dealer)
      embed.add_field(name = "Table", value = table)

    embed.add_field(name = "Game menu", value = game_message)
    if edit:
      await self.message.edit(embed=embed)
    else:
      self.message = await self.channel.send(embed=embed)
  
  async def end_game(self):
    await self.message.clear_reactions()
	try:
    	high = self.calculate_score(self.players[0])
    	winner = self.players[0]
    	for player in self.players:
      		score = self.calculate_score(player)
      	if score[0] > high[0]:
        	high = score
        	winner = player
      	elif score[0] == high[0]:
        	if score[1] == high[1]:
          		high = score
          		winner = player

    	from system import currencysystem as pineapple
    	pineapple.add_currency(winner.user, winner.message.guild, self.table_total)

    	from system import levelsystem, currencysystem
    	await levelsystem.add_exp(self.author, self.channel.guild, win_exp, channel = self.channel)
          
    	hand_type = ['high card', 'one pair', 'two pair', 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush', 'royal flush']
    	message = f'Congratulations <@{winner.mention}>! you have won {self.table_total} pineapple with a {hand_type[high[0] - 1]}'
    	footer = 'Game Over!'
    	await self.generate_embed(game_message=message, footer = footer, end = True)
	except:
		print("it broke")
    position = 0
    await self.mainMessage.delete()
    for game in games:
      if game.author == self.author:
        if game.channel == self.channel:
          games.pop(position)
          return 0
      position += 1

  def calculate_score(self, player):
    table = self.dealer_cards

    highest = 0
    high_card = 0
    
    hand = table + player.cards

    #flush/straight flush/royal flush

    vals = self.count_ranks(hand)
    flush = self.flush(hand)
    straight = self.straight(hand)
    four = int(self.four_kind(vals))
    fh = self.full_house(vals)  
    three = int(self.three_kind(vals))
    two = int(self.two_pair(vals))
    one = int(self.one_pair(vals))
    
    if flush and straight:
      highest = 9 #straight flush
      if straight[0].rank == 14: #royal flush
        highest = 10
      high_card = straight[0]

    elif four > 0: #4 of a kind
      highest = 8
      high_card = four

    elif fh: #full house
      highest = 7
      high_card = fh[0]
    
    elif flush: #flush
      highest = 6
      high_card = flush[0]

    elif straight: #straight
      highest = 5
      high_card = straight[0]

    #3 of a kind
    elif three > 0: #4 of a kind
      highest = 4
      high_card = three
    
    #2 pair
    elif two > 0:
      highest = 3
      high_card = two
      
    #one pair
    elif one > 0:
      highest = 2
      high_card = one

    #high card
    else:
      highest = 1
      high_card = self.high_card(hand)
    
    return [highest, high_card]

  def flush(self, hand):
    nums = [0, 0, 0, 0]
    for card in hand:
      nums[card.suit - 1] = nums[card.suit - 1] + 1

    suit = 1
    for num in nums:
      if num == 5:
        break
      suit = suit + 1

    if suit > 4:
      return None

    ret_hand = []
    for card in hand:
      if card.suit == suit:
        ret_hand.append(card)

    ret_hand.sort()
    
    return ret_hand

  def straight(self, hand):
    ret_hand = hand.copy()
    ret_hand.sort()
    
    one = True
    two = True
    three = True
    
    for i in range(5):
      if ret_hand[i].rank < ret_hand[i+1].rank:
        one = False
        break

    for i in range (1, 6):
      if ret_hand[i].rank < ret_hand[i+1].rank:
        one = False
        break

    for i in range (2, 6):
      if ret_hand[i].rank < ret_hand[i+1].rank:
        one = False
        break

    if one:
      return ret_hand[0:5]
      
    if two:
      return ret_hand[1:6]

    if three:
      return ret_hand[2:]

    return None

  def four_kind(self, ranks):
    rank = 2
    for num in ranks:
      if num == 4:
        return rank
      rank = rank + 1

    return -1

  def full_house(self, ranks):
    curr = 2
    pos = [-1, -1]

    for num in ranks:
      if num == 3:
        pos[0] = curr
      if num == 2:
        pos[1] = curr
      curr = curr + 1

    if pos[0] > 0 and pos[1] > 0:
      return pos
    return None

  def three_kind(self, ranks):
    rank = 2
    for num in ranks:
      if num == 3:
        return rank
      rank = rank + 1

    return -1

  def two_pair(self, ranks):
    rank = 2
    higher = -1
    count = 0
    for num in ranks:
      if num == 2:
        count = count + 1
        if rank > higher:
          higher = rank
      rank = rank + 1

    if count < 2:
      higher = -1
    
    return higher

  def one_pair(self, ranks):
    rank = 2
    higher = -1
    for num in ranks:
      if num == 2:
        if rank > higher:
          higher = rank
      rank = rank + 1

    return higher

  def high_card(self, hands):
    ret_hand = []
    ret_hand.sort()
    return ret_hand[0].rank
    
  def count_ranks(self, hand):
    nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for card in hand:
      rank = card.rank
      nums[rank - 1] = nums[rank - 1] + 1

    return nums