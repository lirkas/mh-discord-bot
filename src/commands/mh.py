import discord
import discord.ext.commands as cmds

import client.utils as utils
import client.bot as bot
import lib.mhutils as mhutils
import lib.textutils as txtutils


#===============================#
#===== MH RELATED COMMANDS =====#
#===============================#

class Mh(cmds.Cog):
    '''
    Contains Monster Hunter related commands\n
    Some commands require monster data to be setup first
    '''
    def __init__(self, bot):
        self.bot = bot

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

        result = mhutils.search_hitzone_data(
                name, mhutils.mhfu_monsters, mhutils.mhfu_monsters_names)
        
        if result.code == mhutils.ResultCode.FOUND_DATA:
            for data in result.content:
                image_path = mhutils.get_hitzone_image(data)
                file = discord.File(image_path, filename='hitzone.png')
                embed = discord.Embed(type='image')
                embed.title = data.header
                embed.set_image(url='attachment://hitzone.png')
                embed.color = 16777215
                embed.set_footer(text=data.footer)

                await ctx.send(files=[file], embeds=[embed])
            return True
        elif result.code == mhutils.ResultCode.FOUND_MANY:
            await ctx.send('```'+result.content+'```')
            return True
        
        else:
            await ctx.send('```'+result.message+'```')
        
        return True