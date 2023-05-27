import system.fileio as fileio
import discord

win_exp = 10
win_curr = 45
win_char = '+'

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
    main = await message.channel.send(message.author.mention + " has started playing hangman.")
    games.append(Hangman())
    await games[-1].hangman_main(message, client, main)

class Hangman:
  async def hangman_main(self, message, client, main):
    self.guessesRemaining = 6
    self.incorrect = []
    self.word = self.rand_word()
    self.channel = message.channel
    self.author = message.author
    self.client = client
    self.mainMessage = main
    
    self.dashes = ""
    for i in range(len(self.word)):
      self.dashes += f'{win_char} '

    self.dashes = self.dashes[:-3]

    embed=discord.Embed(description = "...", color=0xEB459E)
    self.message = await self.channel.send(embed=embed)

    await self.generate_output()

  async def generate_output(self, send = False):
    #output = IMAGES[len(self.incorrect)] + "\n"
    output = self.dashes + "\n"
    output += "Guesses remaining: " + str(self.guessesRemaining - len(self.incorrect)) + "\n"
    output += "Incorrect Guesses: " + str(self.incorrect)[1:-1] 

    embed = self.generate_embed(output)
    if not send:
      await self.message.edit(embed = embed)
    else:
      self.mainMessage = await self.channel.send(self.author.mention + " is continuing hangman.")
      self.message = await self.channel.send(embed = embed)
  
  async def guess_letter(self, guess):
    dashes = self.dashes.strip().replace(" ", "")
    guess = guess.lower()
    if guess[0] in self.dashes or guess[0] in self.incorrect:
      return None
    elif guess[0] in self.word:
      self.dashes = ""
      for i in range(len(dashes)):
        if guess[0] is self.word[i]:
          self.dashes += guess[0] + " "
        else:
          self.dashes += dashes[i] + " "
      self.dashes = self.dashes[:-1]
          
    else:
      self.incorrect.append(guess)

  async def guess_word(self, guess):
    guess = guess.lower()
    guess = guess.strip()
    self.word = self.word.strip()
    if len(guess) is len(self.word) and guess in self.word:
      self.dashes = ""
      for i in range(len(guess)):
        self.dashes += guess[i] + " "
      self.dashes = self.dashes[:-1]
    else:
      self.incorrect.append(guess)

  async def win_output(self, win):
    output = self.dashes + "\n"
    output += "Guesses remaining: " + str(self.guessesRemaining - len(self.incorrect)) + "\n"
    output += "Incorrect Guesses: " + str(self.incorrect)[1:-1] + "\n\n"
    if win:
      output += "You Win!"
      from system import levelsystem, currencysystem
      await levelsystem.add_exp(self.author, self.channel.guild, win_exp, self.channel)
      currencysystem.add_currency(self.author, self.channel.guild, win_curr)
    else: 
      output += "You Lose :(\n"
      output += 'The word was \"' + self.word[:-1] + '\"'
      
    self.message = await self.message.edit(embed=self.generate_embed(output, False, win))
    self.end_game()
    await self.mainMessage.delete()
  
  def rand_word(self):
    dict = fileio.read_data("dictionary.txt", path="games/hangman/")
    import random
    random.shuffle(dict)
    return dict.pop(0)

  async def turn_manager(self, message):
    move = message.content.split(" ")
    length = len(move)
    move.pop(0)

    if length == 1:
      await self.generate_output(send=True)
    else:
      if len(move[0]) == 1:
        await self.guess_letter(move[0])
      else:
        await self.guess_word(move[0])
    await message.delete()

    if not win_char in self.dashes:
      await self.win_output(True)
    elif len(self.incorrect) is self.guessesRemaining:
      await self.win_output(False)
    else:
      await self.generate_output()
      
  def generate_embed(self, output_text, player_turn = True, win = True):
    embed=discord.Embed(description = output_text, color=0xEB459E)
    embed.set_author(name=self.author.display_name + "'s Hangman", icon_url=self.author.avatar_url)
    embed.set_image(url=f'https://www.oligalma.com/downloads/images/hangman/hangman/{len(self.incorrect) + 4}.jpg')
    if player_turn:
      embed.set_footer(text="&hangman [letter]  |  &hangman [word] | &hangman new")
    else:
      embed.set_footer(text="Game Over!  |  &hangman new")
      if win:
        embed.set_image(url="https://media.tenor.com/wO2-bT8eZt8AAAAC/yes-nice.gif")
      else:
        embed.set_image(url="https://media.tenor.com/o5KxLwKlbO0AAAAM/seriously-facepalm.gif")
    return embed

  def end_game(self, win = False):
    position = 0
    for game in games:
      if game.author == self.author:
        if game.channel == self.channel:
          games.pop(position)
          return 0
      position += 1