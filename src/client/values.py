import json


user_not_allowed = "You are not allowed to do that !"
bot_not_allowed = "I am not allowed to do that !"
too_many_args = "Too many arguments !"
not_enough_args = "Not enough arguments !"
wrong_syntax = "Incorrect syntax !"
error = "An error occured !"
unavailable = "Command unavailable for the moment !"

code = "```"

start_info = 30

raw = 0
args = 1
args_info = 2
info = 3
func = 4

mhfu_monster_path = "../files/mhfu/monsters/"
mhfu_sm_monster_path = "../files/mhfu/small_monsters/"

mhp3_monster_path = "../files/mhp3/monsters/"
mhp3_sm_monster_path = "../files/mhp3/small_monsters/"

def get_value(id):

    f = open('../files/config.json', 'r')
    config = ''.join(f.readlines())
    j = json.loads(config)

    value = j[id]

    f.close()
    return value

prefix = get_value('PREFIX')
unknown_cmd = "This command does not exist !\nType `"+prefix+"cmds` to check."

# return icon image ( png format )
def get_icon(name):

    f = open('../files/'+name+'.png', 'rb')
    return f.read()
