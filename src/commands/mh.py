import discord
import discord.ext.commands as cmds

import client.utils as utils
import client.bot as bot
import lib.mhutils as mhutils


#===============================#
#===== MH RELATED COMMANDS =====#
#===============================#

class Mh(cmds.Cog):
    '''defines the class used to create commands'''
    def __init__(self,bot):
        self.bot = bot
        self.monsters = {}
        self.setup_monster_data()

    cls=bot.Command
    
    #=============#
    ## ITEM MHP3 ##
    #=============#
    name='itemp3'
    aliases=['ip3']
    args=['ITEM']
    args_infos=['The item to search for']
    description='[MHP3] Find the possible ways to obtain an item'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_p3(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        result = mhutils.search_item(item, mhutils.mhp3_monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
    
    #=============# 
    ## ITEM MHFU ##
    #=============#
    name='itemfu'
    aliases=['ifu']
    description='[MHFU] Find the possible ways to obtain an item'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_fu(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        result = mhutils.search_item(item, mhutils.mhfu_monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
     
    #=============# 
    ## ITEM MHF1 ##
    #=============#
    name='itemf1'
    aliases=['if1']
    description='[MHF1] Find the possible ways to obtain an item'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_f1(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        result = mhutils.search_item(item, mhutils.mhf1_monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
    
    #=============# 
    ## ITEM MHXX ##
    #=============#
    name='itemxx'
    aliases=['ixx']
    description='[MHXX] Find the possible ways to obtain an item'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_xx(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        result = mhutils.search_item(item, mhutils.mhxx_monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
    

    #================#
    ## MONSTER MHP3 ##
    #================#
    name='monsterp3'
    aliases=['mp3']
    args=['MONSTER','RANK']
    args_infos=['The monster to look for', 'Rank: [1-2][LR][HR]']
    description='[MHP3] Display obtainable items from a specific monster'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_p3(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        result = mhutils.search_monster(name, mhutils.mhp3_monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True
    
    #================#
    ## MONSTER MHFU ##
    #================#
    name='monsterfu'
    aliases=['mfu']
    args_infos=['The monster to look for', 'Rank: [1-2][LR][HR][G]']
    description='[MHFU] Display obtainable items from a specific monster'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_fu(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        result = mhutils.search_monster(name, mhutils.mhfu_monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True


   
    #================#
    ## MONSTER MHF1 ##
    #================#
    name='monsterf1'
    aliases=['mf1']
    args_infos=['The monster to look for', 'Rank: [LR][HR][G]']
    description='[MHF1] Display obtainable items from a specific monster'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_f1(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        result = mhutils.search_monster(name, mhutils.mhf1_monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True
    
    #================#
    ## MONSTER MHXX ##
    #================#
    name='monsterxx'
    aliases=['mxx']
    args_infos=['The monster to look for', 'Rank: [LR][HR][G][?-?]']
    description='[MHXX] Display obtainable items from a specific monster'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_xx(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        result = mhutils.search_monster(name, mhutils.mhxx_monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True
    

    #================#
    ## HITZONE MHFU ##
    #================#
    name='hitzonefu'
    aliases=['hfu']
    args=['MONSTER']
    args_infos=['The monster to look for', 'None']
    description='[MHFU] Display hitzone values for a specific monster'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_hitzone_fu(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        result = mhutils.show_hitzones(
                name, mhutils.mhfu_monsters, mhutils.mhfu_monsters_names)
  
        # sends a message for each result
        for r in result:
            await ctx.send("```\n"+r+"```")

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

