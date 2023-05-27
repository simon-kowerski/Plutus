async def make_channel(guild, name):
  return await guild.create_text_channel(name)
