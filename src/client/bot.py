import discord
import discord.ext.commands as cmds

import client.utils as utils

class Bot(cmds.Bot):
    
    def __init__(self, **options):
        super().__init__(utils.get('PREFIX'), case_insensitive=True, **options)
        self.self_bot = False
        self.formatter = HelpFormatter
        self.activity = discord.Activity(type=1, name='Monster Hunter')
        self.owner_id = utils.get('OWNER_ID')
        self.remove_command('help')
        self.command_not_found = 'Command not found\nCheck the available commands with `'+self.command_prefix+'help`'

    def send_code(self, msg):
        super().send('```'+msg+'```')
    
    
    async def on_command_error(self, ctx, exception):
        cmd = ctx.command

        for i in range(len(exception.args)):
            print(str(i)+' : '+str(exception.args[i]))

        if cmd == None:
            await ctx.send(self.command_not_found)
        else:
            # this is not working - must be fixed asap
            await ctx.invoke(self.get_command('help'), cmd.name)

class Command(cmds.Command):

    def __init__(self, callback, **kwargs):
        super().__init__(callback, **kwargs)
        self.args = kwargs.get('args',[])
        self.args_infos = kwargs.get('args_infos',[])


class HelpFormatter(cmds.DefaultHelpCommand):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def format(self):
        super().format()
        print('format()')

