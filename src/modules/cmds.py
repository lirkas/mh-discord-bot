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

    'itemFU' : (values.prefix+'itemfu',['ITEM'],
        ['The item to find'],
        'Find the possible ways to obtain a monster item (MHFU)',
        commands.find_item_fu),

    'itemP3' : (values.prefix+'itemp3',['ITEM'],
        ['The item to find'],
        'Find the possible ways to obtain a monster item (MHP3)',
        commands.find_item_p3),

    'monsterFU' : (values.prefix+'monsterfu',['MONSTER'],
        ['The monster to find'],
        'See all the possible obtainable items from a monster (MHP3)',
        commands.find_monster_fu),

    'monsterP3' : (values.prefix+'monsterp3',['MONSTER'],
        ['The monster to find'],
        'See all the possible obtainable items from a monster (MHFU)',
        commands.find_monster_p3),
}
