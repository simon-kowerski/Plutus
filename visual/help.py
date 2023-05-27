import discord
#make it so able to pass specific commands to get help on
async def generate_help(message):
  msg = "Tsk tsk...the commands are self explanatory, why do you need more info"
  if "hello" in message.content:
    embed=discord.Embed(title="&help {hello}", description="Just Plutus saying hello!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_image (url="https://media.tenor.com/5iiD6jOOCuAAAAAC/quby-high-five.gif")
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)
  
  elif "profile" in message.content:
    embed=discord.Embed(title="&help {profile}", description="Will let you know the level, exp, currency, and collectables with `&profile @[username]`!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_image (url="https://media.tenor.com/0sRqUfe4XHwAAAAC/duck-cute.gif")
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)
  
  elif "inventory" in message.content:
    embed=discord.Embed(title="&help {inventory}", description="Will show you your collection of collectables obtainable from games and shop!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_image (url="https://media.tenor.com/qAPCIYSsGU4AAAAi/cute.gif")
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)
  
  elif "level" in message.content:
    embed=discord.Embed(title="&help {level}", description="Display your current level and exp with `&level`!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_image (url="https://media.tenor.com/nrrR0__sNeoAAAAi/cute.gif")
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)
    
  elif "blackjack" in message.content:
    embed=discord.Embed(title="&help {blackjack} - Solo", description="Play a game of Blackjack!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.add_field(name="♣️Objective:", value="Attempting to beat the dealer by getting as close to 21 as possible without going over." ,inline=True)
    embed.add_field(name="♦️Scoring:", value="Face cards are worth 10 points, Ace can be either 1 or 11 up to each player, and the rest are its original value." ,inline=True)
    embed.add_field(name="♠️Reward:", value="Beating the dealer will give you 29 Pineapple. If during the start of the round, the player has a natural(Ace and Face Card) dealer will pay you 83 Pineapple. If tied, no Pineapple is given." ,inline=False)
    embed.add_field(name="♥️Deal:", value="Each player will be dealt two cards face up, while the dealer will get one face up, and one face down card." ,inline=False)
    embed.add_field(name="♣️Order:", value="The one who started the game will be first to go, the rest of the players will go in the order of mention." ,inline=False)
    embed.add_field(name="♦️Play:", value="Start the game by sending `&blackjack`, each player will be asked to stand(`&blackjack stand`) or hit(`&blackjack hit`) if their card value is under 21. Stand will end your turn for the round. Hit will give you another card in attemp to get closer or hit 21. If you go over 21, you automatically lose. Start a new game with `&blackjack new`, with confirmation(`&blackjack confirm`) from everyone." ,inline=False)
    await message.channel.send(embed=embed)

  elif "hangman" in message.content:
    embed=discord.Embed(title="&help {hangman} - Solo", description="Play a game of hangman with words from our personal dictionary of more than 61,000+ words!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.add_field(name="Objective:", value="Guessing the word before the image is fully formed." ,inline=False)
    embed.add_field(name="Reward:", value="45 Pineapple for correctly guessing the word." ,inline=False)
    embed.add_field(name="Play:", value="Guess any letter between a-z with `&hangman [letter]`, you will be given 6 guesses. Once you know what the word is, guess the word with `&hangman [word]`. Start a new game with `&hangman new`." ,inline=False)
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)

  elif "poker" in message.content:
    embed=discord.Embed(title="&help {poker} - Multiplayer", description="Play a game of poker with your friends and scam them of their Pineapple!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.add_field(name="♣️Objective:", value="Get a higher poker hand than all the others playing bluffing when needed to make other players fold." ,inline=False)
    embed.add_field(name="♦️Scoring:", value="By the end, you will compare you hand with others. There are 9 different hands that you can end up with each associating with different point values. If multiple people have the same hands, the higher of the hands-Ace being the highest-will have the higher score. \nStraight Flush - Highest possible hand consisting of five cards of the same suit in a sequence. Ex. The highest flush is A, K, Q, J, 10 called a royal flush. \nFour of a Kind - Four of the same value cards. Ex. Four Aces, or four 3s. \nFull House - Three cards of one value, and two cards of another value. Ex. Three Aces and two 6s. \nFlush - Five cards of the same suit, but not in sequence. Ex. Q, 10, 6, 4, 3 of Hearts. \nStraight - Five cards in sequence but not of the same suit. Ex. 9♥, 8♣, 7♠, 6♦, 5♥. \nThree of a Kind - Three cards of the same value and two other cards of different rank. Ex. Three jacks, and seven and a two. \nTwo pairs - Contains one pair of one rank and another pair of a different rank, and a fifth card of a different rank. Ex. Q, Q, 8, 8, 3. \nOne pair - Contain one pair of cards at the same rank, and different everything else. Ex. 10, 10, 3, 7, K." ,inline=False)
    embed.add_field(name="♠️Betting:", value="When beginning the game, first player will be asked to place an initial bid, either small (10 Pineapple) or large (20 Pineapple). Everyone else will have to either match or fold (withdraw). Then the game starts. After the initial three cards are shown, first person will either match (check), or raise (by 10, 20, 30, 40 or 50) and everyone else will either have to match that or raise it more, in which then everyone has to match it again. In any of these, you have the option to fold. Once last card is dealt and everyone have made their bets, those who are left will show their cards and best hand gets all the Pineapple. If there is only one person left as all the rest folded, that person gets all the Pineapple and do not have to show their hand." ,inline=False)
    embed.add_field(name="♣️Deal:", value="Each player will be sent two cards privately, once everyone made their initial bid, three cards will be placed face up on the table. Everyone would have a chance to decided whether they want to raise, match or fold, the next card will be placed on the table and the process repeats until there are five cards on the table." ,inline=False)
    embed.add_field(name="♦️Order:", value="The one who started the game will be last to go, the rest of the players will go in the order of mention." ,inline=False)
    embed.add_field(name="♦️Play: Start the game with a minimum of two players with `&poker @[username]`. After being dmed your cards, you will be asked to put in a small or large bid, by clicking on the reactions that associate with that you will start the game.", value="" ,inline=False)
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)
  
  #elif "slots" in message.content:

  #elif "balance" in message.content:

  #elif "shop" in message.content:

  #elif "daily" in message.content:
  else:
    await message.channel.send(embed=helpmsg1(message))

def helpmsg1(message):
  date = message.created_at
  helpmsg=discord.Embed(title="Command List!", description="For more info on a specific command, send `&help {command}`", color=discord.Color.blurple(), timestamp=date)
  helpmsg.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
  helpmsg.add_field(name="⚙️System", value="`hello`, `profile`, `inventory`, `level`", inline=False)
  helpmsg.add_field(name="🎲Games", value="`blackjack`, `hangman`, `slots`, `poker`", inline=False)
  helpmsg.add_field(name="💵Currency", value="`balance`, `shop`, `daily`", inline=False)
  return helpmsg

#give money to each other
#trade stuff