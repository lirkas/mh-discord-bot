import sys
import os
import asyncio
import logging as log

from aioconsole import ainput
from threading import Thread
import discord

from discord.ext import commands as cmds

import commands.mh as _mh
import commands.util as _util
import commands.admin as _admin

import client.bot as cbot
import client.uinput as uinput
import client.utils as utils


# initialize bot and add commands
client = cbot.Bot()

# initialize UI
ui = uinput.UI(client)

async def setupBot(client):
    await client.add_cog(_util.Util(client))
    await client.add_cog(_admin.Admin(client)) # must be added before Mh cog
    await client.add_cog(_mh.Mh(client))

async def restart():
    os.execv("main.py",[''])

@client.event
async def on_message(message):
    
    ctx = await client.get_context(message)
    await client.invoke(ctx)

    # prints message for console
    ui.display(message)


@client.event
async def read_input():

    while(True):
        line = await ainput()
        try:
            await ui.process(line)
        except BaseException as e:
            print("Error : "+str(e))

@client.event
async def on_ready():
    await setupBot(client)
    print('Logged in as '+client.user.name+' ['+str(client.user.id)+']')
    print('__')
    print('setting up server/channel')
    try:
    #set the channel for the CLI
        print(utils.get('DEFAULT_SERVER'))
    
        ui.server = client.get_guild(int(utils.get('DEFAULT_SERVER')))
        ui.channel = client.get_channel(int(utils.get('DEFAULT_CHANNEL')))

    except AttributeError:
        print("Could not set server and channel")

    asyncio.ensure_future(read_input(), loop=client.loop)

#asyncio.run(setupBot(client))
client.run(utils.get('BOT_TOKEN'))