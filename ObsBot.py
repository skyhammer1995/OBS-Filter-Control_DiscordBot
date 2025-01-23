# ObsBot.py

# OBS websocket docu: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#setsourcefiltersettings
import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from obswebsocket import obsws, requests



# Read from locally maintained .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OBS_HOST = os.getenv('OBS_HOST')
OBS_PORT = os.getenv('OBS_PORT')
OBS_PW = os.getenv('OBS_PW')

# configure and init Discord Bot
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
description = 'Using discord commands and my Insta360 Link camera so you can see whatever you need to play hybrid D&D!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, description=description, help_command=help_command)

# configure and connect OBS Websocket
obs = obsws(OBS_HOST, OBS_PORT, OBS_PW, authreconnect=1)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        obs.connect()
        print("Connected to OBS Websocket")
    except Exception as e:
        print(f"Failed to connect to OBS: {e}")
        await bot.close()

@bot.event
async def on_disconnect():
    """Runs when the bot disconnects from Discord."""
    print("Bot disconnected from Discord.")
    obs.disconnect()

async def obs_enable_filter(filter_name, delay=0.2):
    """Enable a filter on OBS"""
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName=filter_name, 
                                             filterEnabled=True))
    await asyncio.sleep(delay)
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName=filter_name, 
                                             filterEnabled=False))
    await asyncio.sleep(delay)
    
####### Manual cam control commands #######
@bot.command(name='pan+', help='\n -moves camera\'s pan in the positive direction a certain # of degrees; optional: number of iterations')
async def view_pan_positive(ctx, iterations: int = 1):
    try:
        for _ in range(iterations):
            await obs_enable_filter('Pan+')
        await ctx.send(f"Panned+ {iterations} times")
    except Exception as e:
        await ctx.send(f'Error: {e}')

@bot.command(name='pan-', help='\n -moves camera\'s pan in the negative direction a certain # of degrees; optional: number of iterations')
async def view_pan_negative(ctx, iterations = 1):
    try:
        for _ in range(iterations):
            await obs_enable_filter('Pan-')
        await ctx.send(f"Panned- {iterations} times")
    except Exception as e:
        await ctx.send(f'Error: {e}')

@bot.command(name='tilt+', help='\n -moves camera\'s tilt in the positive direction a certain # of degrees; optional: number of iterations')
async def view_tilt_positive(ctx, iterations = 1):
    try:
        for _ in range(iterations):
            await obs_enable_filter('Tilt+')
        await ctx.send(f"Tilted+ {iterations} times")
    except Exception as e:
        await ctx.send(f'Error: {e}')

@bot.command(name='tilt-', help='\n -moves camera\'s tilt in the negative direction a certain # of degrees; optional: number of iterations')
async def view_tilt_negative(ctx, iterations = 1):
    try:   
        for _ in range(iterations):
            await obs_enable_filter('Tilt-')
        await ctx.send(f"Tilted- {iterations} times")
    except Exception as e:
        await ctx.send(f'Error: {e}')

@bot.command(name='zoom+', help='\n -moves camera\'s zoom in the positive direction a certain # of degrees; optional: number of iterations')
async def view_zoom_positive(ctx, iterations = 1):
    try:
        for _ in range(iterations):
            await obs_enable_filter('Zoom+')
        await ctx.send(f"Zoomed+ {iterations} times")
    except Exception as e:
        await ctx.send(f'Error: {e}')

@bot.command(name='zoom-', help='\n -moves camera\'s zoom in the negative direction a certain # of degrees; optional: number of iterations')
async def view_zoom_negative(ctx, iterations = 1):
    try:
        for _ in range(iterations):
            await obs_enable_filter('Zoom-')
        await ctx.send(f"Zoomed- {iterations} times")
    except Exception as e:
        await ctx.send(f'Error: {e}')

####### Preset view commands #######
@bot.command(name='wholeTable', help='\n -moves camera to preset view of the entire table')
async def view_table_whole(ctx):
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName='Whole Table', 
                                             filterEnabled=True))
    response_message = 'Ok dawg, let\'s look at the whole table!'
    await ctx.send(response_message)

@bot.command(name='leftTable', help='\n -moves camera to preset view of the left side of the table')
async def view_table_left(ctx):
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName='Left Table', 
                                             filterEnabled=True))
    response_message = 'Ok dawg, let\'s look at the left side of the table!'
    await ctx.send(response_message)

@bot.command(name='rightTable', help='\n -moves camera to preset view of the right side of the table')
async def view_table_right(ctx):
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName='Right Table', 
                                             filterEnabled=True))
    response_message = 'Ok dawg, let\'s look at the right side of the table!'
    await ctx.send(response_message)

@bot.command(name='DM', help='\n -moves camera to preset view of the DM')
async def view_table_dm(ctx):
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName='DM', 
                                             filterEnabled=True))
    response_message = 'Ok dawg, let\'s look at the DM\'s mug!'
    await ctx.send(response_message)

@bot.command(name='battlemap', help='\n -moves camera to preset view of the battlemap area of the table')
async def view_table_battlemap(ctx):
    obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                             filterName='Battlemap', 
                                             filterEnabled=True))
    response_message = 'Ok dawg, let\'s look at the action!'
    await ctx.send(response_message)

bot.run(TOKEN)
