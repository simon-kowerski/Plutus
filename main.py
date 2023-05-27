import discord
from discord.ext import commands
import os

from visual import messagehandler as mhandler
from visual import reactionhandler as rhandler
from system import onstartup as start
from system import guildtools as gtool

intents = discord.Intents.all()

client = discord.Client(intents=intents)
#client = commands.Bot(command_prefix = '&', intents = intents)

print('Starting System...')

@client.event
async def on_ready():
  await client.user.edit(username = "Plutus")
  await start.on_ready(client)

@client.event
async def on_message(message):
  await mhandler.on_message(message, client)

#adding and removing guilds
@client.event
async def on_guild_join(guild):
  await gtool.new_guild_setup(guild)

@client.event
async def on_guild_remove(guild):
  await gtool.leave_guild_procedure(guild)

#adding users
#users dont get removed from file when they leave server
@client.event
async def on_member_join(member):
  await gtool.new_member(member)
  
@client.event
async def on_reaction_add(reaction, user):
  await rhandler.on_reaction_add(reaction, user, client)
"""
  saving data even after bot is stopped from running
  files whenever joining server created
  on name change, change server name
  users stuff
""" 
#bye bye

#start the bot:
try:
    client.run(os.environ['bot_token'])
except:
    os.system("kill 1")