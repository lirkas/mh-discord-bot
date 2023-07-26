import os
import logging as log

import asyncio

import discord

import commands.mh as _mh
import commands.util as _util
import commands.admin as _admin

import client.bot as cbot
import client.utils as utils

import lib.logutils as logutils


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
    print(utils.format_message(message))
    ctx = await client.get_context(message)
    await client.invoke(ctx) 

@client.event
async def on_error(event, *args, **kwargs):
    logutils.handle_error('../files/.log')

@client.event
async def on_ready():
    await setupBot(client)
    print('Logged in as '+client.user.name+' ['+str(client.user.id)+']')
    print('------------------------------------')

async def main():
    '''
    Entry point, where the client attemps to authenticate and connect to
    discord.
    '''
    try:
        logger.info('starting authentication with token')
        await client.login(utils.get('BOT_TOKEN'))
    except discord.LoginFailure as e :
        logger.error('Invalid token')
        if not client.is_closed():
            logger.info('Closing client')
            await client.close()
            raise e
        return
    
    try:
        await client.connect()
    except discord.ConnectionClosed as e:
        logger.info('Client connection closed: '+str(e.code))
        logger.info(e.reason)

# easier login
# client.run(utils.get('BOT_TOKEN'), log_level=log.WARNING)