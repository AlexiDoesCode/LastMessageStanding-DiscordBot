import asyncio
import random

from discord.ext import commands
import discord

client = discord.Client()
token = ''
bot = commands.Bot(command_prefix='!')

challenge_channel = 'DISCORD_CHANNEL_ID'
global t
global started
global ot
started = False

max_range = 900
min_range = 1
life = True


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    while life:
        await updateStatus()


@bot.command(name='start')
async def start(ctx, s):
    if ctx.message.author.guild_permissions.administrator:
        try:
            number_check = int(s)
        except ValueError:
            await ctx.send("That's not a number.")
            return False
        s = int(s)

        if s > max_range:
            await ctx.send("The number you picked is too high, maximum is " + str(max_range))
            return False
        if s < min_range:
            await ctx.send("The number you picked is too low, minimum is " + str(min_range))
            return False

        global started
        global ot
        ot = s
        started = True
        await ctx.send("Starting a timer for " + str(s) + " seconds")
        await countdown(s)

        started = False
        channel = client.get_channel(challenge_channel)
        messages = await ctx.channel.history(limit=1).flatten()
        discord_id = messages[0].author.id
        await ctx.send("Winner! <@" + str(discord_id) + ">")
    else:
        await ctx.send("You don't have permissions to do that :P Nice try though ;)")


async def countdown(s):
    global t
    t = int(s)
    while t:
        await asyncio.sleep(1)
        t -= 1


@bot.event
async def on_message(message):
    global t
    global started
    if message.author == client.user:
        return
    if message.author.bot:
        return
    if started:
        if message.channel.id == challenge_channel:
            t = int(ot)
            return True
    await bot.process_commands(message)

    return None



if __name__ == '__main__':
    bot.run(token)
