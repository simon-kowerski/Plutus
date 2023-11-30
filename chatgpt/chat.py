import os
import openai

#Get latest version from git hub
#python setup.py install

openai.organization = os.environ['chatgpt_orgid']
openai.api_key = os.environ['chatgpt_key']
MODEL_ENGINE = "gpt-3.5-turbo"

async def handle_input(channel, message):
  msg = message.content[6:] 
  if len(msg) < 2:
    msg = 'I am incredibly foolish and forgot to include a message here'
  if str(msg).startswith("clear"):
    clear(message)
    return
  path = 'chatgpt/'
  filename = str(message.author.id)

  start = True
  if os.path.exists(path + filename):
    start = False
  file = open(path + filename, "a")
  if start:
    train = open(path+"training.txt", "r")
    file.write(train.read())
  file.close()
  file = open(path + filename, "r+")

  
  con_hist = file.read()
  new_hist = await generate(msg, con_hist, str(message.author.id), channel)
  if os.path.exists(path + filename):
    os.remove(path + filename)

  file.close()
  file = open(path + filename, "a")
  file.write(new_hist)

def clear(message):
  path = 'chatgpt/'
  filename = str(message.author.id) 
  import os
  if os.path.exists(path + filename):
    os.remove(path + filename)

def get_response(prompt):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return chat_completion.choices[0].message.content

async def generate(
               input_str,
    conversation_history,
                USERNAME, 
                 channel):
    # Update the conversation history
    conversation_history += f'USER: {input_str}\n'
   
    # Generate a response using GPT-3
    message = get_response(conversation_history)

    if message.startswith("GPT: "):
      message = message[5:]
      try:
        if message.index("GPT: "):
          message = message[message.index("GPT:") + 5:]
      except:
        pass

    # Update the conversation history
    conversation_history += f'GPT: {message}\n'

    # send the response
    #await channel.send(message)
    await channel.send("OpenAI integration currently unavailable. Check the project development page on GitHub for updates.")
    
    return conversation_history
