import os
import discord
import json
import os
import string
from discord.ext import commands
from discord import DMChannel
import threading
import asyncio

#asyncio.get_event_loop().set_debug(True)





intents = discord.Intents.default()
intents.presences = True ##->> all this is required

prefix = "-"

setuprunning = True
setupprogress = 0

ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DECIMAL_DIGITS = "0123456789"
ALPHABETS = ASCII_LOWERCASE + ASCII_UPPERCASE



from webserver import keep_alive


#
# error handling
#
async def error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You didnt give the arguments properly, try using help')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have manage_messages permssion')


#
#Reuseable funcs
#

async def msg_random_channel(guild,msg):
for i in guild.text_channels:
    if i.permissions_for(guild.me).send_messages:
      await i.send(msg)
      break



#
#commands here
#



if os.environ.get('BOT_TOKEN') is not None:
  my_secret = os.environ['BOT_TOKEN']
else:
    if os.path.exists("token.txt") == False:
        tok = open("token.txt","w")
        tok.write("put your token here")
        tok.close
        print("please put token in token.txt or add Evironment Variable called 'BOT_TOKEN' containing the token")
        exit()
    else:
        my_secret = open("token.txt","r")
        my_secret = my_secret.read()

client = discord.Client()
bot = commands.Bot(command_prefix=prefix)





#Check if user is mod
async def check_mod(ctx):
  try:
    serverfile = open("servers/" + str(ctx.message.guild.id)+ ".json","r")
    serverconfig = json.open(serverfile)
    modrole = serverconfig["mod"]
    return(True)
  except:
    await ctx.send("setup mod role. eg:\n -setup mod <role name or id>\n this tells the bot which role to check for when using the bot")
    return(False)





#Check prefix of individual server
def check_prefix(ctx):
  try:
    serverfile = open("servers/" + str(ctx.author.guild.id)+ ".json","r")
    serverconfig = json.load(serverfile)
    cprefix = str(serverconfig["prefix"])
    c = list(str(cprefix))
    c = c[len(c) - 1]
    if c not in ALPHABETS:
      return(cprefix)
    else:
      return(str(cprefix + " "))
  except:
    return(prefix)





@bot.event
async def on_message(ctx):
  if ctx.content.startswith('ping'):
    await ctx.channel.send('pong')
  if ctx.content.startswith('vc'):
    await ctx.channel.send('use prefix (probably -)')
  print(ctx.guild.name,"    ",ctx.author," : ",ctx.content)
  cprefix = check_prefix(ctx)
  bot.command_prefix = str(cprefix)
  await bot.process_commands(ctx)





@bot.event
async def on_guild_join(guild):
  print("Joined new server: ",guild.name)
  msg = 'Thanks for adding me!\n you can ask an admin to setup this bot using `-setup` and use `-help` for help'
  msg_random_channel(guild,msg)
  





@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))





#called when user joins vc
@bot.event
async def on_voice_state_update(member, before, after):
  if not before.channel and after.channel:
    role = discord.utils.get(member.guild.roles, name="role name")
    await member.edit(mute=False)

@on_voice_state_update.error
async def error(ctx,error):
  if isinstance(error, discord.errors.Forbidden):
    print(ctx,error)




@bot.command(name='mute')
async def mute(ctx, member : discord.Member):
    checkrole1 = check_mod(ctx)
    try:
      if checkrole1:
          role = discord.utils.get(ctx.guild.roles, name="Muted")
          await ctx.channel.send(ctx.author.name + " Muted " + str(member.name))
          await member.add_roles(role)
      if checkrole1 == False:
          await ctx.channel.send("hey you dont have a Mod role")
    except:
      await ctx.channel.send('This server doesnt have a configured mute role, or i cant manage roles!')





@bot.command(name='unmute')
async def unmute(ctx, member : discord.Member):
  checkrole1 = check_mod(ctx)
    try:
      if checkrole1:
          role = discord.utils.get(ctx.guild.roles, name="Muted")
          await ctx.channel.send(ctx.author.name + " unmuted " + str(member.name))
          await member.remove_roles(role)
      if checkrole1 == False:
          await ctx.channel.send("you dont have the Mod role")
    except:
      await ctx.channel.send('This server doesnt have a configured mute role!')






@bot.command(name='vcmute')
async def vcmuteall(ctx):
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=True)
            print('muted ',member)
        print('muted everyone in ',vc)
    else:
        await ctx.channel.send("you dont have Mod role")





@bot.command(name='vcunmute')
async def vcunmuteall(ctx):
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)
            print('unmuted ',member)
        print('unmuted everyone in ',vc)
    if checkrole1 not in sender.roles:
        await ctx.channel.send("you dont have the Mod role")




@bot.command(name='vcmove',description='to specify the channels, you can use "" ',help='move the person to specified vc')
async def vcmove(ctx, members:commands.Greedy[discord.Member], *, channel:discord.VoiceChannel):
  try:
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        for member in members:
            await member.move_to(channel=channel)
    else:
        await ctx.channel.send("you dont have Mod role")
  except discord.ext.commands.errors.MissingRequiredArgument:
    await ctx.channel.send("Missing Argument")

@vcmove.error
async def on_error(ctx, error):
  await error_handler(ctx,error)

@bot.command(name='vcmoveall',discription='to specify the channels, you can use "" ',help='moves an entire vc to another')
async def vcmoveall(ctx, channel1:discord.VoiceChannel, channel2:discord.VoiceChannel):
  sender:discord.Member = ctx.author
  checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
  members = channel1.members
  if checkrole1 in sender.roles:
      for member in members:
          await member.move_to(channel=channel2)
  else:
      await ctx.channel.send("you dont have Mod role")

@vcmoveall
async def on_error(ctx, error):
  await error_handler(ctx,error)





@bot.command(name='servernum',help='shows how many people added me to their server')
async def servers(ctx):
    print("\n")
    servers = list(bot.guilds)
    await ctx.send(f"Connected on {str(len(servers))} servers")
    for i in servers:
        print(i.name,"  ",i.id)
    print("\n")





@bot.command(name='serverlist',description='only for devs')
async def serversall(ctx):
  servers = list(bot.guilds)
  for server in servers:
    print(server.name,": \n")
    for channel in server.text_channels:
      print("    ",channel.name)
    print("\n\n")





@bot.command(command="setup",help='setup the bot')
async def setup(ctx,prop=None,value=None):
  #only runs if the user is administrator
  if ctx.message.author.guild_permissions.administrator:
    if value:
      try:
        serverfile = open("servers/" + str(ctx.message.guild.id)+  ".json","r")
      except:
        serverfile = open("servers/" + str(ctx.message.guild.id)+ ".json","w")
    
      try:
        serverconfig = json.load(serverfile)
      except:
        serverconfig = {}
      print(serverconfig)
      if prop == "mod" or prop == "mute":
        checkrole1 = discord.utils.get(ctx.guild.roles, name = value)
        if checkrole1 == None:
          checkrole1 = ctx.guild.get_role(int(value))
        if checkrole1 != None:
          serverconfig[prop] = checkrole1.id
          await ctx.send(prop + " is now " + str(checkrole1.name))
        else:
          await ctx.send("That Role Doesnt Exist")
      else:
        serverconfig[str(prop)] = str(value)
        await ctx.send(str(prop)+" is now "+str(value))
      serverfile = open("servers/" + str(ctx.message.guild.id) + ".json","w")
      serverconfig = json.dump(serverconfig,serverfile,indent=4)
    else:
      await ctx.send("How to use:\nFirst of all after -setup you have to give it two arguements, one for the property and other for the properties value. for eg:\n-setup mod <name or id of mod role>\n for now these are the properties that have a meaning:\nmod\nprefix\nmute")
  else:
    await ctx.channel.send("get an admin to do this")





keep_alive()
bot.run(str(my_secret))