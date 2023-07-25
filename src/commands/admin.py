import os

import discord.ext.commands as cmds

import client.utils as utils
import client.bot as bot
import lib.mhutils as mhutils
import lib.textutils as txtutils


class Admin(cmds.Cog):
    '''defines the class used to create commands'''
    def __init__(self, bot: bot.Bot):
        self.bot = bot
        self.setup()
        self.setup_monster_data()

    cls=bot.Command

    #================#
    ## RELOAD DATA  ##
    #================#
    name='reload'
    aliases=['rdata']
    args=['GAME']
    args_infos=['The game to reload data for (Optional)']
    description='[ADMIN] Reload monster data'
    hidden=True
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases, hidden=hidden)
    async def reload_data(self, ctx: cmds.Context):

        # only bot owner can do that
        if ctx.author.id == self.bot.owner_id:
            self.setup_monster_data()
            await ctx.send('```Sucessfully reloaded monster data```')
        else:
            await ctx.send('```Bot-owner only command```')
        
        return True
    
    
    def setup_monster_data(self):
        '''Initializes monster data used for all commands'''

        # retreive paths from config file
        mhf1_sm_monster_path = utils.get('MHF1_SM_MONSTER_PATH')
        mhf1_monster_path = utils.get('MHF1_MONSTER_PATH')
        mhfu_sm_monster_path = utils.get('MHFU_SM_MONSTER_PATH')
        mhfu_monster_path = utils.get('MHFU_MONSTER_PATH')
        mhp3_sm_monster_path = utils.get('MHP3_SM_MONSTER_PATH')
        mhp3_monster_path = utils.get('MHP3_MONSTER_PATH')
        mhxx_monster_path = utils.get('MHXX_MONSTER_PATH')

        mhutils.mhf1_monsters = mhutils.files_to_list(mhf1_sm_monster_path)
        mhutils.mhf1_monsters.update(mhutils.files_to_list(mhf1_monster_path))

        mhutils.mhfu_monsters = mhutils.files_to_list(mhfu_sm_monster_path)
        mhutils.mhfu_monsters.update(mhutils.files_to_list(mhfu_monster_path))
        mhutils.mhfu_monsters_names = mhutils.create_monster_list(mhutils.mhfu_monsters)

        mhutils.mhp3_monsters = mhutils.files_to_list(mhp3_sm_monster_path)
        mhutils.mhp3_monsters.update(mhutils.files_to_list(mhp3_monster_path))

        mhutils.mhxx_monsters = mhutils.files_to_list(mhxx_monster_path)

    def setup(self):
        '''Initializes various stuffs used in commands'''

        default_font = utils.get('DEFAULT_FONT')
        image_path = utils.get('IMG_PATH')

        txtutils.default_font = default_font
        txtutils.default_image_path = image_path

        # create the img directory if it doesnt exist yet
        if not os.path.isdir(image_path):
            os.makedirs(image_path)

        # Testing ascii support for text tables
        if not txtutils.test_ascii_support():
            txtutils.extended_ascii_support = False