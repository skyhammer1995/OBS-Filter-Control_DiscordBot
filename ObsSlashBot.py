# ObsBot.py
# OBS websocket docu: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#setsourcefiltersettings
import asyncio
import os
import discord
from re import match
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
from obswebsocket import obsws, requests

# Read from locally maintained .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
RSPCHNL = os.getenv('DISCORD_RSPCHNL')
OBS_HOST = os.getenv('OBS_HOST')
OBS_PORT = os.getenv('OBS_PORT')
OBS_PW = os.getenv('OBS_PW')

ChannelResponseId = int(RSPCHNL) # D&D Galtea::camera-control
GuildId = int(GUILD_ID)

# configure and init Discord Bot
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
description = 'Using discord commands and my Insta360 Link camera so you can see whatever you need to play hybrid D&D!'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents, description=description, help_command=help_command)
# tree = discord.app_commands.CommandTree(bot)

# configure and connect OBS Websocket
obs = obsws(OBS_HOST, OBS_PORT, OBS_PW, authreconnect=1)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        obs.connect()
        print("Connected to OBS Websocket")
    except Exception as e:
        print(f"Failed to connect: {e}")
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

@bot.tree.command(name='ping')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong")

####### Manual cam control commands #######
@bot.tree.command(name='manual_camera_control')
@app_commands.describe(cam_control='Different methods of manually controlling the camera')
@app_commands.choices(cam_control=[
    app_commands.Choice(name='up', value=1),
    app_commands.Choice(name='down', value=2),
    app_commands.Choice(name='left', value=3),
    app_commands.Choice(name='right', value=4),
    app_commands.Choice(name='in', value=5),
    app_commands.Choice(name='out', value=6)
])
@app_commands.describe(iterations='How many times do you want to enact your momvement?')
async def manual_camera_control(interaction: discord.Interaction, cam_control:app_commands.Choice[int], iterations: int = 1):
    obsFilterName: str
    try:
        match cam_control.value:
            case 1:
                obsFilterName = 'Tilt+'
            case 2:
                obsFilterName = 'Tilt-'
            case 3:
                obsFilterName = 'Pan-'
            case 4:
                obsFilterName = 'Pan+'
            case 5:
                obsFilterName = 'Zoom+'
            case 6:
                obsFilterName = 'Zoom-'
            case _:
                print('Default Case')
                raise Exception("cam_control must be one of the choices provided")
        for _ in range(iterations):
            await obs_enable_filter(obsFilterName)
        await interaction.response.send_message(f"Applied {obsFilterName} {iterations} times", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}', ephemeral=True)

####### Preset view commands #######
@bot.tree.command(name='preset_camera_view') #Show
@app_commands.describe(preset= 'Choose a preset view you\'d like')
@app_commands.choices(preset=[
    app_commands.Choice(name='Whole Table', value=1),
    app_commands.Choice(name='Left Table', value=2),
    app_commands.Choice(name='Right Table', value=3),
    app_commands.Choice(name='DM', value=4),
    app_commands.Choice(name='Battlemap', value=5)
])
async def preset_view_control(interaction: discord.Interaction, preset:app_commands.Choice[int]):
    responseChannel = bot.get_channel(ChannelResponseId) 
    try:
        obs.call(requests.SetSourceFilterEnabled(sourceName='Insta360 Link', 
                                                 filterName=preset.name, 
                                                 filterEnabled=True))
        await interaction.response.send_message(f'Ok Dawg, let\'s look at {preset.name}')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')

@bot.command()
async def sync(ctx):
    bot.tree.copy_global_to(guild=ctx.guild)
    await ctx.bot.tree.sync(guild=ctx.guild) 

bot.run(TOKEN)
