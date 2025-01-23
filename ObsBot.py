# ObsBot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from obswebsocket import obsws, requests

intents = discord.Intents.default()
intents.message_content = True

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
bot = commands.Bot(command_prefix='!', intents=intents, description=description, help_command=help_command)

# configure and connect OBS Websocket
async def connect_to_obs():
    obs = obsws(OBS_HOST, OBS_PORT, OBS_PW)
    obs.connect()
    
    return obs

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

####### Preset view commands #######
@bot.command(name='wholeTable', help='\n -moves camera to preset view of the entire table')
async def view_table_whole(ctx):
    obs = await connect_to_obs()
    obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                filter_name='wholeTable', 
                                                filter_enabled=True))
    response_message = 'Ok dawg, let\'s look at the whole table!'
    await ctx.send(response_message)
    obs.disconnect()

@bot.command(name='leftTable', help='\n -moves camera to preset view of the left side of the table')
async def view_table_left(ctx):
    obs = await connect_to_obs()
    obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                filter_name='leftTable', 
                                                filter_enabled=True))
    response_message = 'Ok dawg, let\'s look at the left side of the table!'
    await ctx.send(response_message)
    obs.disconnect()

@bot.command(name='rightTable', help='\n -moves camera to preset view of the right side of the table')
async def view_table_right(ctx):
    obs = await connect_to_obs()
    obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                filter_name='rightTable', 
                                                filter_enabled=True))
    response_message = 'Ok dawg, let\'s look at the right side of the table!'
    await ctx.send(response_message)
    obs.disconnect()

@bot.command(name='DM', help='\n -moves camera to preset view of the DM')
async def view_table_dm(ctx):
    obs = await connect_to_obs()
    obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                filter_name='DM', 
                                                filter_enabled=True))
    response_message = 'Ok dawg, let\'s look at the DM\'s mug!'
    await ctx.send(response_message)
    obs.disconnect()

@bot.command(name='battlemap', help='\n -moves camera to preset view of the battlemap area of the table')
async def view_table_battlemap(ctx):
    obs = await connect_to_obs()
    obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                filter_name='battlemap', 
                                                filter_enabled=True))
    response_message = 'Ok dawg, let\'s look at the action!'
    await ctx.send(response_message)
    obs.disconnect()

####### Manual cam control commands #######
@bot.command(name='pan+', help='\n -moves camera\'s pan in the positive direction a certain # of degrees; optional: number of iterations')
async def view_pan_positive(ctx, amountOfIterations = 1):
    obs = await connect_to_obs()
    try:
        for _ in range(amountOfIterations):
            obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                        filter_name='Pan+', 
                                                        filter_enabled=True))
        response_message = 'panning+ ' + str(amountOfIterations) + ' times'
        await ctx.send(response_message)
    except Exception as e:
        await ctx.send(f'Error: {e}')
    obs.disconnect()

@bot.command(name='pan-', help='\n -moves camera\'s pan in the negative direction a certain # of degrees; optional: number of iterations')
async def view_pan_negative(ctx, amountOfIterations = 1):
    obs = await connect_to_obs()
    try:
        for _ in range(amountOfIterations):
            obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                        filter_name='Pan-', 
                                                        filter_enabled=True))
        response_message = 'panning- ' + str(amountOfIterations) + ' times'
        await ctx.send(response_message)
    except Exception as e:
        await ctx.send(f'Error: {e}')
    obs.disconnect()

@bot.command(name='tilt+', help='\n -moves camera\'s tilt in the positive direction a certain # of degrees; optional: number of iterations')
async def view_tilt_positive(ctx, amountOfIterations = 1):
    obs = await connect_to_obs()
    try:
        for _ in range(amountOfIterations):
            obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                        filter_name='Tilt+', 
                                                        filter_enabled=True))
        response_message = 'tilt+ ' + str(amountOfIterations) + ' times'
        await ctx.send(response_message)
    except Exception as e:
        await ctx.send(f'Error: {e}')
    obs.disconnect()

@bot.command(name='tilt-', help='\n -moves camera\'s tilt in the negative direction a certain # of degrees; optional: number of iterations')
async def view_tilt_negative(ctx, amountOfIterations = 1):
    obs = await connect_to_obs()
    try:   
        for _ in range(amountOfIterations):
            obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                        filter_name='Tilt-', 
                                                        filter_enabled=True))
        response_message = 'tilt- ' + str(amountOfIterations) + ' times'
        await ctx.send(response_message)
    except Exception as e:
        await ctx.send(f'Error: {e}')
    obs.disconnect()

@bot.command(name='zoom+', help='\n -moves camera\'s zoom in the positive direction a certain # of degrees; optional: number of iterations')
async def view_zoom_positive(ctx, amountOfIterations = 1):
    obs = await connect_to_obs()
    try:
        for _ in range(amountOfIterations):
            obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                        filter_name='Zoom+', 
                                                        filter_enabled=True))
        response_message = 'zoom+ ' + str(amountOfIterations) + ' times'
        await ctx.send(response_message)
    except Exception as e:
        await ctx.send(f'Error: {e}')
    obs.disconnect()

@bot.command(name='zoom-', help='\n -moves camera\'s zoom in the negative direction a certain # of degrees; optional: number of iterations')
async def view_zoom_negative(ctx, amountOfIterations = 1):
    obs = await connect_to_obs()
    try:
        for _ in range(amountOfIterations):
            obs.call(requests.SetSourceFilterVisibility(source_name='Insta360 Link', 
                                                        filter_name='Zoom-', 
                                                        filter_enabled=True))
        response_message = 'zoom- ' + str(amountOfIterations) + ' times'
        await ctx.send(response_message)
    except Exception as e:
        await ctx.send(f'Error: {e}')
    obs.disconnect()

bot.run(TOKEN)
