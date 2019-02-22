

from operator import attrgetter

import discord
import discord.ext.commands as cmds

import client.bot as bot


class Util:

    def __init__(self, bot):
        self.bot = bot
    
    # defines the class used to create commands
    cls=bot.Command
    
    #====================#
    ## DISPLAY COMMANDS ##
    #====================# 
    name='cmds'
    description='Display all the available commands'
    @cmds.command(cls=cls, name=name, description=description)
    async def show_commands(ctx):
        cmds = ctx.bot.commands
        prefix = ctx.bot.command_prefix
        await ctx.send('```'+get_commands(list(cmds),prefix=prefix)+'```')

    #================# 
    ## HELP COMMAND ##
    #================#

    # displays help for a specific command
    name='help'
    args=['COMMAND']
    args_infos=['The command to get help from']
    description='Display help for a specific command'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description)
    async def help(ctx):
     
        msg = ctx.message
        cmds = ctx.bot.commands
        prefix = ctx.bot.command_prefix
        
        try:
            cmd = msg.content.split()[1]
        except IndexError:
        # if no command has been requested - display all commands
            await ctx.send('```'+get_commands(list(cmds),prefix=prefix)+'```')
            return True

        cmd_name = cmd.lower().replace(ctx.bot.command_prefix,'',1)
        infos = ''
    
        cmd = ctx.bot.get_command(cmd_name)
        # check if the command exists
        if cmd == None:
            await ctx.send(cmd_name+' is not a valid command')
            return
        else:    
            infos += 'Usage: '+prefix+cmd.name+' '
        
            # insert args for the specified command
            for arg in cmd.args:
                infos += arg+' '

            infos += '\n- '+cmd.description+'\n'
            # display each argument with its infos
            for i in range(len(cmd.args)):
                line = '\n\t'+cmd.args[i]
            
                # add spaces for pretty print
                while len(line) < 16 :
                    line += ' '
            
                infos += line+' : '+cmd.args_infos[i]

        await ctx.send('```'+infos+'```')


# returns a string that contains all commands found in the list
def get_commands(cmdlist, prefix=''):
    
    cmdlist = sorted(cmdlist, key=attrgetter('name'))

    msg = ''
    for cmd in cmdlist:
        
        txt = prefix+cmd.name
        for alias in cmd.aliases:
            txt += '|'+alias

        # insert args for the specified command
        for arg in cmd.args:
            txt += " "+arg

        # add spaces for pretty print
        while len(txt) < 30:
            txt += " "

        txt += ": "+cmd.description+"\n"
        msg += txt

    return msg
