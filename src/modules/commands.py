import discord

import client.values as values
import client.utils as utils
import lib.mhutils as mhutils


#===============================#
#===== MH RELATED COMMANDS =====#
#===============================#

# look for a specific item on a specific game
async def find_item_p3(**kwargs):
    await find_item(**kwargs, game='P3')
    return ''
async def find_item_fu(**kwargs):
    await find_item(**kwargs, game='FU')
    return ''
async def find_item(**kwargs):
    game = kwargs['game'] 

    channel = kwargs['message'].channel
    args = kwargs['args']
    #game = args[len(args)-1]
    # use this when we can check about args
    #args.remove(args[len(args)-1])
    item = ' '.join(args)

    if game == 'FU':
        monsters = mhutils.files_to_list(values.mhfu_sm_monster_path)
        monsters.update(mhutils.files_to_list(values.mhfu_monster_path))
    elif game == 'P3':
        monsters = mhutils.files_to_list(values.mhp3_sm_monster_path)
        monsters.update(mhutils.files_to_list(values.mhp3_monster_path))

    result = mhutils.search_item(item, monsters)
    
    for r in result:
        await channel.send("```\n"+r+"```")
    
    return ''


# look for a specific monster
async def find_monster_fu(**kwargs):
    await find_monster(**kwargs, game='FU')
    return ''

async def find_monster_p3(**kwargs):
    await find_monster(**kwargs, game='P3')
    return ''

async def find_monster(**kwargs):
    game = kwargs['game'] 
    if game != None:
        print("Game = "+game)

    channel = kwargs['message'].channel
    args = kwargs['args']
    #game = args[len(args)-1]
    # use this when we can check about args
    #args.remove(args[len(args)-1])
    name = ' '.join(args)
    
    if game == 'FU':
        monsters = mhutils.files_to_list(values.mhfu_sm_monster_path)
        monsters.update(mhutils.files_to_list(values.mhfu_monster_path))
    elif game == 'P3':
        monsters = mhutils.files_to_list(values.mhp3_sm_monster_path)
        monsters.update(mhutils.files_to_list(values.mhp3_monster_path))


    result = mhutils.search_monster(name, monsters)
    
    for r in result:
        await channel.send("```\n"+r+"```")

    return 'ok'
        
#=================#
#===== INFOS =====#
#=================#

async def get_commands(**kwargs):
    
    cmdlist = kwargs['cmdlist']
    msg = values.code

    for c in cmdlist:

        txt = cmdlist[c][values.raw]+" "

        # insert args for the specified command
        for arg in cmdlist[c][values.args]:
            txt += arg+" "

        # add spaces for pretty print
        while len(txt) < 30:
            txt += " "

        txt += ": "+cmdlist[c][values.info]+"\n"
        msg += txt

    return msg+values.code

# show infos for a specific command
async def command_info(**kwargs):
    
    try:
        cmd = kwargs['args'][0].lower().replace(values.prefix,'',1)
    except IndexError:
        return 'Missing argument'

    infos = ''

    
    cmds = kwargs['cmdlist']
    # check if the command exists
    if cmd not in cmds.keys():
        return cmd+' is not a valid command'
    else:    
        infos += 'Usage: '+cmd+' '
        
        # insert args for the specified command
        for arg in cmds[cmd][values.args]:
            infos += arg+' '

        infos += '\n- '+cmds[cmd][values.info]+'\n'
        # display each argument with its infos
        for i in range(len(cmds[cmd][values.args_info])):
            line = '\n\t'+cmds[cmd][values.args][i]
            
            # add spaces for pretty print
            while len(line) < 16 :
                line += ' '
            
            infos += line+' : '+cmds[cmd][values.args_info][i]

    return '```'+infos+'```'

#========================#
#===== COMMAND PROC =====#
#========================#
#
# process the command the user requested
async def process(**kwargs):

    msg = values.unknown_cmd
    message = kwargs['message']
    channel = message.channel
    client = kwargs['client']
    cmdlist = kwargs['cmdlist']

    # extract arguments from the command line
    args = message.content.split( )
    
    # extract the command
    cmd = args[0].lower()
    args.remove(args[0])
        
    # now check if the command does exist
    for c in list(cmdlist.values()):
        
        # if the command exists - execute it
        if cmd == c[values.raw]:
            msg = await c[values.func](**kwargs, args=args)
    # if empty message - dont send
    if msg == '':
        return

    await channel.send(msg)


# the following method is executed whenever a user adds a reaction
async def process_reaction(**kwargs):

    client = kwargs['client']
    reaction = kwargs['reaction']
    message = reaction.message
    user = kwargs['user']

    #await message.remove_reaction(reaction.emoji, user)
