import discord

async def store():
  msg = "Tsk tsk...the commands are self explanatory, why do you need more info"
  if "hello" in message.content:
    embed=discord.Embed(title="&help {hello}", description="Just Plutus saying hello!", color=discord.Color.blurple())
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_image (url="https://media.tenor.com/5iiD6jOOCuAAAAAC/quby-high-five.gif")
    embed.set_footer(text=msg)
    await message.channel.send(embed=embed)