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
    
    if os.path.exists('../files/config_.json'):
        f = open('../files/config_.json', 'r')
    else:
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
