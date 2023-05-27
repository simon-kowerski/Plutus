from system import filetools as ftool
from system import fileio as fio
from os import system as sys 

#when the bot first comes online
async def on_ready(client):
  guild = client.guilds[0]
  sys('clear')
  print(f'Logged in as {client.user}')
  print(f'Servers:')
  for guild in client.guilds:
    print(f'{guild.name}')

  #ensures that each guild the bot is in has a file
  for guild in client.guilds:
    ftool.make_file(guild.name, "a")
    await fio.write_usernames(guild)