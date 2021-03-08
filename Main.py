import discord
import json
import os
from discord.ext import commands
prefix = "-"

if os.path.exists("token.txt") == False:
    tok = open("token.txt","w")
    tok.write("put your token here")
    tok.close

token = open("token.txt","r")

client = discord.Client()
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_message(context):
    if context.content.startswith('ping'):
        await context.channel.send('pong')
    print(context.author," : ",context.content)
    await bot.process_commands(context)



@bot.command(name='mute')
async def mute(context, member : discord.Member):
    sender:discord.Member = context.author
    checkrole1 = discord.utils.get(context.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        role = discord.utils.get(context.guild.roles, name="Muted")
        await context.channel.send(context.author.name + " Muted " + str(member.name))
        await member.add_roles(role)

@bot.command(name='unmute')
async def unmute(context, member : discord.Member):
    sender:discord.Member = context.author
    checkrole1 = discord.utils.get(context.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        role = discord.utils.get(context.guild.roles, name="Muted")
        await context.channel.send(context.author.name + " unmuted " + str(member.name))
        await member.remove_roles(role)




bot.run(token.read())