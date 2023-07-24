import os
import json

import discord


# attempts to extract the discord user id
# return int
def get_uid(string):

    # try to see if the string is already the uid
    try:
        uid = int(string)
    except ValueError:
        False
    else:
        return uid
    
    # if its a mention
    if string.startswith('<@'):
        # make sure its a mention
        try:
            return int(string[2:len(string)-1])
        except ValueError:
            return ""


# fetch a value with the given ID from a file
def get(id):
    
    # get the token from env - heroku compat
    if id == 'BOT_TOKEN':
        if id in os.environ.keys():
            return os.environ.get(id)

    if os.path.exists('../files/config_.json'):
        f = open('../files/config_.json', 'r')
    else:
        f = open('../files/config.json', 'r')

    config = ''.join(f.readlines())
    j = json.loads(config)

    # fallback if a key is not found in the user defined config file
    if id not in j and f.name == '../files/config_.json':
        f = open('../files/config.json', 'r')
        config = ''.join(f.readlines())
        j = json.loads(config)

    value = j[id]

    f.close()
    return value

# return icon image ( png format )
def get_icon(name):

    f = open('../files/'+name+'.png', 'rb')
    return f.read()

def format_message(message: discord.Message) -> str:
    '''
    Formats a message to be displayed as plain text in a file or terminal\n
    Can display date, time, server, channel, username and message content (if text)
    '''
    text_message = ''
    message_date = message.created_at

    date = '{d}-{m}-{y}'.format(
        d=str(message_date.day).zfill(2),
        m=str(message_date.month).zfill(2),
        y=str(message_date.year))
    
    time = '{h}:{m}'.format(
        h=str(message_date.hour).zfill(2),
        m=str(message_date.minute).zfill(2))
    
    # Add ansi color codes for a nice look
    text_message += '\033[30m['+date+']['+time+']\033[0m'
    text_message += '\033[32m['+message.guild.name+']\033[0m'
    text_message += '\033[33m['+message.channel.name+']\033[0m '
    text_message += '\033[36m'+message.author.name+'\033[0m : '
    text_message += message.content

    # replacing code syntax characters with newlines
    # message content will always be displayed under the message info  
    text_message = text_message.replace('```\n', '\n')
    text_message = text_message.replace('\n```', '\n')
    text_message = text_message.replace('```', '\n')

    return text_message