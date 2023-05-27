path = "system/ServerFiles/"
numofvals=3

###############
#####WRITE#####
###############
async def write_usernames(guild):
  read = open(path + guild.name)
  exists = read.read()
  read.close()
  
  async for user in guild.fetch_members():
    if user.name not in exists:
      add_user(user, guild)

  read = read_data(guild.name)
  read = split_user_scores(read[0])
  add_vaules_to_guild(guild, numofvals - len(read))
  
  
def add_user(user, guild):
  file = open(path + guild.name, "a")
  output = user.name + "#"
  for i in range(numofvals):
    output += " 0"
  file.write(output + "\n") 
  file.close()

def append_to_file(filename, text):
  file = open(path+filename, "a")
  file.write(str(text) + "")
  file.close()

#takes in array of values and writes it to the file
def update_file(filename, newdata):
  with open(path+filename, 'w', encoding='utf-8') as file:
    file.writelines(newdata)

################
######READ######
################
#linefromfile is string with a single line from the file
#returns an array with the numbers in the file as ints
def split_user_scores(linefromfile):
  linefromfile = linefromfile.split("#")
  if not len(linefromfile) == 0:
    linefromfile.pop(0)
  linefromfile = linefromfile[0].split(" ")
  linefromfile.pop(0)
  temp = len(linefromfile)
  linefromfile[temp-1] = linefromfile[temp-1][:-1]
  return list(map(int, linefromfile))

#take name (str), and scores (int arr), and combines to be added back to file
def remake_user_line(name, scores):
  ret = ""
  ret += name + "# "
  for val in scores:
    ret += str(val) + " "
  ret = ret[:-1]
  ret += "\n"
  return ret

#returns array with strings for each line that can be editeded 
def read_data(filename, path=path):
  with open(path+filename, 'r', encoding='utf-8') as file:
    return file.readlines()

def add_vaules_to_guild(guild, num):
  data = read_data(guild.name)
  for i in range(len(data)):
    data[i] = data[i][:-1]
    for x in range(num):
      data[i] += " " + str(0)
    data[i] += "\n"

  update_file(guild.name, data)