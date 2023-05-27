from system import channeltools as chtool
from system import filetools as ftool
from system import fileio as fio

channelname = "plutussuperchannel"

async def new_guild_setup(guild):
  print(f'Joined guild: {guild.name}')
  
  #make file for guild
  ftool.make_file(guild.name, "a")
  await fio.write_usernames(guild)  
  
  #make channel for bot bot things
  botchannel = channelname
  channel_exists = False
  for channel in guild.text_channels:
    if channel.name == botchannel:
      channel_exists = True

  if not channel_exists:
    channel = await chtool.make_channel(guild, botchannel)
    fio.append_to_file(guild.name, channel.id)

  #send help command
  await channel.send('&help')

async def leave_guild_procedure(guild):
  ftool.remove_file(guild.name)

async def new_member(member):
  fio.add_user(member, member.guild)