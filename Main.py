import os
import discord
import json
import os
from discord.ext import commands
import thread
prefix = "-"

setuprunning = True
setupprogress = 0

from webserver import keep_alive

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
    if cprefix.endswith(' '):
      pass
    else:
      cprefix = cprefix + " "
    return(cprefix)
  except:
    return(prefix)


@bot.event
async def on_message(ctx):
  if ctx.content.startswith('ping'):
    await ctx.channel.send('pong')
  print(ctx.guild.name,"    ",ctx.author," : ",ctx.content)
  cprefix = check_prefix(ctx)
  bot.command_prefix = str(cprefix)
  await bot.process_commands(ctx)


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
  if not before.channel and after.channel:
    role = discord.utils.get(member.guild.roles, name="role name")
    await member.edit(mute=False)

@bot.command(name="h")
async def help(ctx):
    helpfile = open("help.txt","r")
    await ctx.channel.send(helpfile.read())

@bot.command(name='mute')
async def mute(ctx, member : discord.Member):
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await ctx.channel.send(ctx.author.name + " Muted " + str(member.name))
        await member.add_roles(role)
    if checkrole1 == False:
        await ctx.channel.send("hey you dont have a Mod role")

@bot.command(name='unmute')
async def unmute(ctx, member : discord.Member):
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await ctx.channel.send(ctx.author.name + " unmuted " + str(member.name))
        await member.remove_roles(role)
    if checkrole1 not in sender.roles:
        await ctx.channel.send("you dont have the Mod role")

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

@bot.command(name='vcmove')
async def vcmove(ctx, members:commands.Greedy[discord.Member], *, channel:discord.VoiceChannel):
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        for member in members:
            await member.move_to(channel=channel)
    else:
        await ctx.channel.send("you dont have Mod role")

@bot.command(name='vcmoveall')
async def vcmoveall(ctx, channel1:discord.VoiceChannel, channel2:discord.VoiceChannel):
    sender:discord.Member = ctx.author
    checkrole1 = discord.utils.get(ctx.guild.roles, name = "Mod")
    members = channel1.members
    if checkrole1 in sender.roles:
        for member in members:
            await member.move_to(channel=channel2)
    else:
        await ctx.channel.send("you dont have Mod role")

@bot.command(name='serverlist',help='shows how many people added me to their server')
async def servers(ctx):
    print("\n")
    servers = list(bot.guilds)
    await ctx.send(f"Connected on {str(len(servers))} servers")
    for i in servers:
        print(i.name)
    print("\n")

@bot.command(name='serverlistmore',help='only for devs')
async def serversall(ctx):
  servers = list(bot.guilds)
  for server in servers:
    print(server.name,": \n")
    for channel in server.text_channels:
      print("    ",channel.name)
    print("\n\n")

@bot.command(command="setup",help='not working')
async def setup(ctx,prop=None,value=None):
  if value:
    try:
      serverfile = open("servers/" + str(ctx.message.guild.id)+ ".json","r")
    except:
      serverfile = open("servers/" + str(ctx.message.guild.id)+ ".json","w")
    
    try:
      serverconfig = json.load(serverfile)
    except:
      serverconfig = {}
    print(serverconfig)
    if prop == "mod":
      checkrole1 = discord.utils.get(ctx.guild.roles, name = value)
      if checkrole1 == None:
        checkrole1 = ctx.guild.get_role(int(value))
      if checkrole1 != None:
        serverconfig["mod"] = checkrole1.id
        await ctx.send("mod is now "+str(checkrole1.name))
      else:
        print(checkrole1)
        await ctx.send("That Role Doesnt Exist")
    else:
      serverconfig[str(prop)] = str(value)
      await ctx.send(str(prop)+" is now "+str(value))
    serverfile = open("servers/" + str(ctx.message.guild.id)+ ".json","w")
    serverconfig = json.dump(serverconfig,serverfile,indent=4)
  else:
    await ctx.send("How to use:\nFirst of all after -setup you have to give it two arguements, one for the property and other for the properties value. for eg:\n-setup mod Mod")

keep_alive()
bot.run(str(my_secret))