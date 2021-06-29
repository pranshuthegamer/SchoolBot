import discord
import json
import os
from discord.ext import commands
prefix = "-"

if os.path.exists("token.txt") == False:
    tok = open("token.txt","w")
    tok.write("put your token here")
    tok.close
    print("please put token in token.txt")
    exit()


token = open("token.txt","r")

client = discord.Client()
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_message(context):
    if context.content.startswith('ping'):
        await context.channel.send('pong')
    elif context.content.startswith('dick'):
        await context.channel.send('dock')
    print(context.author," : ",context.content)
    await bot.process_commands(context)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        role = discord.utils.get(member.guild.roles, name="role name")
        await member.edit(mute=False)

@bot.command(name='mute')
async def mute(context, member : discord.Member):
    sender:discord.Member = context.author
    checkrole1 = discord.utils.get(context.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        role = discord.utils.get(context.guild.roles, name="Muted")
        await context.channel.send(context.author.name + " Muted " + str(member.name))
        await member.add_roles(role)
    if checkrole1 not in sender.roles:
        await context.channel.send("hey you dont have a Mod role")

@bot.command(name='unmute')
async def unmute(context, member : discord.Member):
    sender:discord.Member = context.author
    checkrole1 = discord.utils.get(context.guild.roles, name = "Mod")
    if checkrole1 in sender.roles:
        role = discord.utils.get(context.guild.roles, name="Muted")
        await context.channel.send(context.author.name + " unmuted " + str(member.name))
        await member.remove_roles(role)
    if checkrole1 not in sender.roles:
        await context.channel.send("you dont have the Mod role")

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


bot.run(token.read())