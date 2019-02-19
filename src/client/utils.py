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
