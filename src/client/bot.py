import discord
import discord.ext.commands as cmds

import client.utils as cutils

class Bot(cmds.Bot):
    
    def __init__(self, **options):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            cutils.get('PREFIX'), 
            case_insensitive=True, 
            intents=intents, 
            **options)
        self.formatter = HelpFormatter
        self.activity = discord.Activity(type=1, name='Monster Hunter')
        self.owner_id = cutils.get('OWNER_ID')
        self.remove_command('help')
        self.command_not_found = 'Command not found\nCheck the available commands with `'+self.command_prefix+'help`'

    def send_code(self, msg):
        super().send('```'+msg+'```')
    
    
    async def on_command_error(self, ctx, exception):
        cmd = ctx.command

        for i in range(len(exception.args)):
            print(str(i)+' : '+str(exception.args[i]))

        if cmd == None:
            print('Command does not exist')
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

