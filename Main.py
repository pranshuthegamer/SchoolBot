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
async def on_message(ctx):
    if ctx.content.startswith('ping'):
        await ctx.channel.send('pong')
    elif ctx.content.startswith('dick'):
        await ctx.channel.send('dock')
    print(ctx.author," : ",ctx.content)
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
    if checkrole1 not in sender.roles:
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


bot.run(token.read())
