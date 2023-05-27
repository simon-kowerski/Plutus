async def on_reaction_add(reaction, user, client):
  if reaction.message.author != client.user: #only reads reactions added to plutus messages
    return 
  if user == client.user:
    return
  
  if reaction.message.embeds :
    if 'Poker' in str(reaction.message.embeds[0].author):
      import games.poker.poker as poker
      await poker.handle_input(client, reaction=reaction, user=user)