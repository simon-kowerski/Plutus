from system import fileio as file
import discord


#returns new balance
def add_currency(user, guild, amount):
    filelines = file.read_data(guild.name)

    userpos = 0
    for i in range(len(filelines)):
        if user.name in filelines[i]:
            userpos = i
            break

    userline = file.split_user_scores(filelines[userpos])
    userline[2] += amount

    filelines[userpos] = file.remake_user_line(user.name, userline)
    file.update_file(guild.name, filelines)


#spends currency, returns new balance
def spend_currency(user, guild, amount):
    filelines = file.read_data(guild.name)

    userpos = 0
    for i in range(len(filelines)):
        if user.name in filelines[i]:
            userpos = i
            break

    userline = file.split_user_scores(filelines[userpos])

    userline[2] -= amount

    filelines[userpos] = file.remake_user_line(user.name, userline)
    file.update_file(guild.name, filelines)
    return userline[2]


def get_currency(user, guild):
    filelines = file.read_data(guild.name)

    userpos = 0
    for i in range(len(filelines)):
        if user.name in filelines[i]:
            userpos = i
            break

    userline = file.split_user_scores(filelines[userpos])
    return userline[2]


async def display_balance(user, channel):
  filelines = file.read_data(channel.guild.name)

  userpos = 0
  for i in range(len(filelines)):
    if user.name in filelines[i]:
      userpos = i
      break

  userline = file.split_user_scores(filelines[userpos])

  pineapple = userline[2]

  embed = discord.Embed(color=discord.Color.blurple())
  embed.set_author(name="Bank Account for " + user.display_name, icon_url=user.avatar_url)
  embed.add_field(name="Balance", value=str(pineapple) + " Pineapple", inline=False)
  embed.set_image(url="https://media.tenor.com/jv5D1w6ghk4AAAAi/yay-joy.gif")

  await channel.send(embed=embed)
