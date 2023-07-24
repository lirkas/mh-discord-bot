import os
import logging as log

import discord

import commands.mh as _mh
import commands.util as _util
import commands.admin as _admin

import client.bot as cbot
import client.utils as utils


# initialize bot and add commands
client = cbot.Bot()

async def setupBot(client):
    await client.add_cog(_util.Util(client))
    await client.add_cog(_admin.Admin(client)) # must be added before Mh cog
    await client.add_cog(_mh.Mh(client))

async def restart():
    os.execv("main.py",[''])

@client.event
async def on_message(message: discord.Message):
    
    ctx = await client.get_context(message)
    await client.invoke(ctx) 


@client.event
async def on_ready():
    await setupBot(client)
    print('Logged in as '+client.user.name+' ['+str(client.user.id)+']')
    print('------------------------------------')

client.run(utils.get('BOT_TOKEN'))