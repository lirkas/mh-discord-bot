import discord
import discord.ext.commands as cmds

import client.utils as utils
import client.bot as bot
import lib.mhutils as mhutils


#===============================#
#===== MH RELATED COMMANDS =====#
#===============================#

# retreive paths from config file
mhf1_sm_monster_path = utils.get('MHF1_SM_MONSTER_PATH')
mhf1_monster_path = utils.get('MHF1_MONSTER_PATH')
mhfu_sm_monster_path = utils.get('MHFU_SM_MONSTER_PATH')
mhfu_monster_path = utils.get('MHFU_MONSTER_PATH')
mhp3_sm_monster_path = utils.get('MHP3_SM_MONSTER_PATH')
mhp3_monster_path = utils.get('MHP3_MONSTER_PATH')
mhxx_monster_path = utils.get('MHXX_MONSTER_PATH')

class Mh(cmds.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.monsters = {}

    # defines the class used to create commands
    cls=bot.Command
    
    #=============#
    ## ITEM MHP3 ##
    #=============#
    name='itemp3'
    aliases=['ip3']
    args=['ITEM']
    args_infos=['The item to search for']
    description='Find the possible ways to obtain an item (MHP3)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_p3(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        monsters = mhutils.files_to_list(mhp3_sm_monster_path)
        monsters.update(mhutils.files_to_list(mhp3_monster_path))

        result = mhutils.search_item(item, monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
    
    #=============# 
    ## ITEM MHFU ##
    #=============#
    name='itemfu'
    aliases=['ifu']
    description='Find the possible ways to obtain an item (MHFU)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_fu(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        monsters = mhutils.files_to_list(mhfu_sm_monster_path)
        monsters.update(mhutils.files_to_list(mhfu_monster_path))
        
        result = mhutils.search_item(item, monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
     
    #=============# 
    ## ITEM MHF1 ##
    #=============#
    name='itemf1'
    aliases=['if1']
    description='Find the possible ways to obtain an item (MHF1)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_f1(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        monsters = mhutils.files_to_list(mhf1_sm_monster_path)
        monsters.update(mhutils.files_to_list(mhf1_monster_path))
        
        result = mhutils.search_item(item, monsters)
        
        for r in result:
            await ctx.send("```\n"+r+"```")
        
        return True
    
    #=============# 
    ## ITEM MHXX ##
    #=============#
    name='itemxx'
    aliases=['ixx']
    description='Find the possible ways to obtain an item (MHXX)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_item_xx(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        item = ' '.join(args)

        monsters = mhutils.files_to_list(mhxx_monster_path)
        
        result = mhutils.search_item(item, monsters)
        
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
    description='Display obtainable items from a specific monster (MHP3)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_p3(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        monsters = mhutils.files_to_list(mhp3_sm_monster_path)
        monsters.update(mhutils.files_to_list(mhp3_monster_path))
        result = mhutils.search_monster(name, monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True
    
    #================#
    ## MONSTER MHFU ##
    #================#
    name='monsterfu'
    aliases=['mfu']
    args_infos=['The monster to look for', 'Rank: [1-2][LR][HR][G]']
    description='Display obtainable items from a specific monster (MHFU)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_fu(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        monsters = mhutils.files_to_list(mhfu_sm_monster_path)
        monsters.update(mhutils.files_to_list(mhfu_monster_path))
        result = mhutils.search_monster(name, monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True


   
    #================#
    ## MONSTER MHF1 ##
    #================#
    name='monsterf1'
    aliases=['mf1']
    args_infos=['The monster to look for', 'Rank: [LR][HR][G]']
    description='Display obtainable items from a specific monster (MHF1)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_f1(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        monsters = mhutils.files_to_list(mhf1_sm_monster_path)
        monsters.update(mhutils.files_to_list(mhf1_monster_path))
        result = mhutils.search_monster(name, monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True
    
    #================#
    ## MONSTER MHXX ##
    #================#
    name='monsterxx'
    aliases=['mxx']
    args_infos=['The monster to look for', 'Rank: [LR][HR][G][?-?]']
    description='Display obtainable items from a specific monster (MHXX)'
    @cmds.command(cls=cls, name=name, args=args, args_infos=args_infos, description=description, aliases=aliases)
    async def find_monster_xx(self,ctx):
        
        args = ctx.message.content.split()
        args.pop(0)
        name = ' '.join(args)

        monsters = mhutils.files_to_list(mhxx_monster_path)
        result = mhutils.search_monster(name, monsters)
    
        for r in result:
            await ctx.send("```\n"+r+"```")

        return True
