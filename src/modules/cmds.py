import modules.commands as commands
import client.values as values

# list that contains the command structure
# 
# cmd_name :
#   ( prefix + cmd , [args...],
#   [args_info...],
#   cmd_info,
#   cmd_method, is_available)
#

cmdlist = {

    'cmds' :
        (values.prefix+'cmds', [],
        [],
        'Display all commands',
        commands.get_commands),
    
    'help' :
        (values.prefix+'help', ['COMMAND'],
        ['The command you need help with'],
        'Display infos for a specific command',
        commands.command_info),

    'itemfu' : (values.prefix+'itemfu',['ITEM'],
        ['The item to find'],
        'Find the possible ways to obtain a monster item (MHFU)',
        commands.find_item_fu),

    'itemp3' : (values.prefix+'itemp3',['ITEM'],
        ['The item to find'],
        'Find the possible ways to obtain a monster item (MHP3)',
        commands.find_item_p3),

    'monsterfu' : (values.prefix+'monsterfu',['MONSTER', 'RANK'],
        ['The monster to look for', 'Rank: [1-2][LR][HR][G]'],
        'See all the possible obtainable items from a monster (MHFU)',
        commands.find_monster_fu),

    'monsterp3' : (values.prefix+'monsterp3',['MONSTER', 'RANK'],
        ['The monster to look for', 'Rank: [1-2][LR][HR]'],
        'See all the possible obtainable items from a monster (MHP3)',
        commands.find_monster_p3),
}
