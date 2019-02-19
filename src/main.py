import sys
import os
import asyncio
import logging as log

from aioconsole import ainput
from threading import Thread

import modules.cmds as cmds
import modules.commands as commands

import client.uinput as uinput
import client.values as values
import discord


# Logs discord events into a file
logger = log.getLogger('discord')
handler = log.FileHandler(filename='discord.log', encoding='utf-8', mode='w') 
handler.setFormatter(log.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')) 
logger.addHandler(handler)


TOKEN = values.get_value('BOT_TOKEN')
PREFIX = values.prefix


client = discord.Client()

ignore_bot = True

async def restart():
    await client.close()
    os.execv("main.py",[''])

@client.event
async def on_message(message):

    print(message.author.name+" : "+message.content)

    if message.author == client.user and ignore_bot:
        return
    #Check if the message starts with the defined prefix
    if (message.content.startswith(values.prefix) == False):
        return


    #Get function related to cmd if it exists
    await commands.process(message=message, client=client, cmdlist=cmds.cmdlist)

    #await util.check_afk(client, message)

@client.event
async def on_reaction_add(reaction, user):

    if user != client.user or ignore_bot == False:
        await commands.process_reaction(reaction=reaction, user=user, client=client)


@client.event
async def read_input():

    while(True):
        line = await ainput()
        try:
            await uinput.process(client, line)
        except BaseException as e:
            print("Error : "+str(e))

@client.event
async def read_input_debug():

    while(True):
        line = await ainput()
        await uinput.process(client, line)


@client.event
async def on_error(event, *args, **kwargs):
    
    message = args[0]
    channel = message.channel
    exc_info = sys.exc_info()

    print("ERROR :")
    print("Event : "+str(event))
    print("message_id = "+str(message.id))
    print(str(exc_info))
    await channel.send("ERROR: "+str(exc_info[1]))


@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' ['+str(client.user.id)+']')
    print('__________________________________________')

    game_obj = discord.Activity(type=2, name='you' )
    await client.change_presence(activity=game_obj)

    try:
        #set the channel where the bot will speak
        uinput.server = client.get_guild(542599193127026698)
        uinput.channel = uinput.server.get_channel(542599193626411009)
    except AttributeError:
        print("Could not set server and channel")

    # allow the bot_owner to input text
    asyncio.ensure_future(read_input(), loop=client.loop)

client.run(TOKEN)
