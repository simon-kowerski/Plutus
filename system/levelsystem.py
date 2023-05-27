from system import fileio as file
import discord

#def level up
#take in a user and a guild
#access their file and change it 
async def level_up(user, guild, channel):
  filelines = file.read_data(guild.name)

  userpos = 0
  for i in range(len(filelines)):
    if user.name in filelines[i]:
      userpos = i
      break

  userline = file.split_user_scores(filelines[userpos])
  userline[0] += 1
  newlevel = userline[0]
  userline = file.remake_user_line(user.name, userline)

  filelines[userpos] = userline
  file.update_file(guild.name, filelines)

  if channel is not None:
    embed=discord.Embed(description=user.display_name + " has reached level " + str(newlevel) + "!", color=discord.Color.blurple())
    embed.set_author(name="Congratulations!", icon_url=user.avatar_url)
    await channel.send(embed = embed)

#def add exp
#take in a user, guild, and exp amount 
#check for if level up
async def add_exp(user, guild, amount, channel = None):
  filelines = file.read_data(guild.name)

  userpos = 0
  for i in range(len(filelines)):
    if user.name in filelines[i]:
      userpos = i
      break
  
  userline = file.split_user_scores(filelines[userpos])
  userline[1] += amount
  
  filelines[userpos] = file.remake_user_line(user.name, userline)
  file.update_file(guild.name, filelines)
  
  while userline[1] >= level_cap(userline[0]):
    await level_up(user, guild, channel)
    filelines = file.read_data(guild.name)
    userline = file.split_user_scores(filelines[userpos])

def level_cap(level):
  level += 1
  num = level * 100
  for temp in range(level - 1, 0, -1):
    num += temp * 100
  return num

async def display_level(user, channel):
	filelines = file.read_data(channel.guild.name)

	userpos = 0
	for i in range(len(filelines)):
		if user.name in filelines[i]:
			userpos = i
			break

	userline = file.split_user_scores(filelines[userpos])

	exp = userline[1]
	level = userline[0]

	embed=discord.Embed(color=discord.Color.blurple())
	embed.set_author(name="Stats for " + user.display_name, icon_url=user.avatar_url)
	embed.add_field(name="Level", value=str(level), inline=False)
	embed.add_field(name="Experience", value=str(exp) + " / " + str(level_cap(level)), inline=False)
	embed.set_image(url="https://images-ext-1.discordapp.net/external/HQYQ9U3Qx40qZugTNq6ErH9g1mJ9ObGBUYuEU-opznU/https/imgur.com/irIdEv2.gif");

	await channel.send(embed=embed)