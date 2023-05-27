import discord

from visual import help
from system import levelsystem as level
from system import currencysystem as currency
from chatgpt import chat

from games.blackjack import blackjack
from games.hangman import hangman
from games.poker import poker

#messages
async def on_message(message, client):
  msg = message.content.split(' ')[0]
  msg = msg.lower()
  if msg.startswith('&'):
    # from chatgpt import chat
    await level.add_exp(message.author, message.guild, 1, message.channel)
    if "hello" in msg:
      await message.channel.send('Hello! Thanks for saying hi!')
    elif "help" in msg:
      await help.generate_help(message)
    elif "blackjack" in msg:
      await blackjack.handle_input(message, client)
    elif "hangman" in msg:
      await hangman.handle_input(message, client)
    elif "poker" in msg:
      await poker.handle_input(client, message=message)
    elif "level" in msg:
      await level.display_level(message.author, message.channel)
    elif "balance" in msg:
      await currency.display_balance(message.author, message.channel)
    elif "chat" in msg:
      try:
        await chat.handle_input(message.channel, message)
      except:
        await message.channel.send('OpenAI usage limit for the minute reached. Try again when the clock changes.')
    else: 
      await message.channel.send('What')
