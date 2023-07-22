import os
import json
import logging as log

import lib.utils as utils
import lib.textutils as txtutils

files_path = '../files'
mhfu_path = files_path+'/mhfu'
star = "☆"

# used for JSON values
star_1_2 = "1-2 Star"
low_rank = "Low-Rank"
high_rank = "High-Rank"
g_rank = "G-Rank"

lv_1_3 = 'Lv 1~3'
lv_1_4 = 'Lv 1~4'
lv_4_5 = 'Lv 4~5'
lv_5_8 = 'Lv 5~8'
lv_6_8 = 'Lv 6~8'
lv_9_10 = 'Lv 9~10'
lv_11_12 = 'Lv 11~12'
lv_13_15 = 'Lv 13~15'
lv_ex = 'Lv Ex'

mhp3 = "MHP3"
mhfu = "MHFU"
mhf1 = 'MHF1'
mhxx = 'MHXX'

rank_suffix = {
    '1-2'   : star_1_2,
    'LR'    : low_rank,
    'HR'    : high_rank,
    'G'     : g_rank,
    
    '1-3'   : lv_1_3,
    '1-4'   : lv_1_4,
    '4-5'   : lv_4_5,
    '5-8'   : lv_5_8,
    '6-8'   : lv_6_8,
    '9-10'  : lv_9_10,
    '11-12' : lv_11_12,
    '13-15' : lv_13_15,
    'EX'    : lv_ex,
}

_rank_suffix = ['1-2','LR','HR','G']


wordlist_12 = ["1-2","1/2", '1-2 star']
wordlist_lr = ["village","village/low","village/low-rank","low","low-rank","lr"]
wordlist_hr = ["high","hr","high-rank"]
wordlist_g = ["g","g-rank",'g-class']

wordlist_1_3 = ['1~3']
wordlist_1_4 = ['1~4']
wordlist_4_5 = ['4~5']
wordlist_5_8 = ['5~8']
wordlist_6_8 = ['6~8']
wordlist_9_10 = ['9~10']
wordlist_11_12 = ['11~12']
wordlist_13_15 = ['13~15']
wordlist_ex = ['ex']

wordlist_p3 = ["p3","mhp3"]
wordlist_fu = ["fu","mhfu"]
wordlist_f1 = ['f1','mhf1']
wordlist_xx = ['xx','mhxx']

dmg_type_cut = 'CUT'
dmg_type_impact = 'IMP'
dmg_type_shot = 'SHOT'

dmg_type_fire = 'FIR'
dmg_type_water = 'WTR'
dmg_type_thunder = 'THN'
dmg_type_dragon = 'DRG'
dmg_type_ice = 'ICE'
dmg_stagger = 'STAGGER'

wordlist_rank = wordlist_12+wordlist_lr+wordlist_hr+wordlist_g+wordlist_1_4+wordlist_5_8+wordlist_9_10+wordlist_11_12+wordlist_13_15+wordlist_ex
wordlist_game = wordlist_fu+wordlist_p3+wordlist_f1+wordlist_xx


log.basicConfig(level='ERROR')


# check the term and return the rank if it does match any
def check_rank(terms): 
    
    log.info('checking rank: '+str(terms))
    if terms == None:
        return None
    rank = terms.lower()

    # check if the word is one of em - if true - skip
    if rank in wordlist_12:
        return star_1_2
    elif rank in wordlist_lr:
        return low_rank
    elif rank in wordlist_hr:
        return high_rank
    elif rank in wordlist_g:
        return g_rank
    elif '~' in rank:
        return 'Lv '+rank
    elif rank in wordlist_ex:
        return lv_ex
    else:
        log.debug(rank+' is not a valid rank')
        return None

class Drop:
    'Defines item structure'

    def __init__(self, name, rate, qty):
        self.name = name
        self.rate = rate
        self.qty = qty

        self.dict = {}
        self.dict['name'] = self.name
        self.dict['qty'] = self.qty
        self.dict['rate'] = self.rate


    def __str__(self):
        return '{ \'name\': \''+self.name+'\', \'qty\': '+str(self.qty)+', \'rate\': '+str(self.rate)+' }'

    def show(self):
        return ''+self.name+' x'+str(self.qty)+' ('+str(self.rate)+'%)'

class Stats:
    'Stats or related monster combat infos'

    def __init__(self):
        self.parts: list[Part] = []
        self.modes: list[str] = []
        self.notes: dict[str,str] = {}
        self.rage_multiplier = 1.0

class Part:

    def __init__(self, name):
        self.name = name
        self.hitzone_values: list[HitzoneValues] = []
        self.stagger = -1
        
class HitzoneValues:

    def __init__(self, mode):
        self.mode: str = mode

        self.impact = -1
        self.cut = -1
        self.shot = -1
        self.fire = -1
        self.water = -1
        self.thunder = -1
        self.ice = -1
        self.dragon = -1

class Monster:
    'Defines monster structure'

    def __init__(self, name, game, tid = -1):
        self.tid = tid
        self.name = name
        self.game = game

        # contains all rank appearances
        self.ranks = []
        # contains all drop categories
        self.categories = []
        # contains all drops for a category
        self.drops = {}
        # contains various stats such as hitzone values
        self.stats : Stats = None
        # structure :
        # categores['shiny-drop'] = drops
        # ranks['low-rank'] = categories['shiny-drop']

        #print("Monster "+name+" "+game+" has been created")

    def add_drop(self, rank, category, drop):

        # if a dict does not exist for this rank - create it
        if rank not in self.drops.keys():
            
            #print(rank+" not found")
            self.ranks.append(rank)
            self.drops[rank] = {}

        if category not in self.drops[rank].keys():
    
            #print(category+" not found")
            if category not in self.categories:
                self.categories.append(category)
            self.drops[rank][category] = []


        self.drops[rank][category].append(drop)

        #print("Added "+drop.__str__()+" element for "+category)

    def add_drops(self, rank, category, drop_list):
       for drop in drop_list:
           self.add_drop(self, rank, category, drop)

    def find_item(self, item_name):

        name = item_name.lower()
        results = ""

        for rank in self.ranks:
            for cat in self.categories:

                # if the category does not exist for this rank
                try:
                    self.drops[rank][cat]
                except KeyError:
                    log.warning('no ('+cat+') for '+self.name+' '+rank+'')
                    continue

                for drop in self.drops[rank][cat]:
                    if name == drop.name.lower():
                        results = results+'\n  ['+rank+'] '+drop.name+' x'+str(drop.qty)+' ('+str(drop.rate)+'%) - '+cat
        return results
  
    # return a dict with the drops for each rank
    def get_drops(self, rank):
        
        if rank not in self.ranks:
            return rank+" does not exist"

        s = ""
        s += star+" "+self.name+" "+star+"\n"
        s += "\n["+rank+"]\n"
        for cat in self.categories:
            s += "\n\t"+cat+"\n\n"
            for drop in self.drops[rank][cat]:
                s+= "\t\t"+drop.show()+"\n"

        return s

    # display the monster
    def show(self, rank=None):
        
        # un-needed but keep it for the record
        #r = check_rank(rank)
        r = rank

        # if the rank does not exist
        if r != None and r not in self.ranks:
            log.warning(r+' for '+self.name+' does not exist')
            return ['\nNo data for '+self.game+' '+r+' '+self.name]
        log.debug('rank set to '+str(r))

        s = ""
        result = []

        for _rank in self.ranks:
        
            # if the rank does not match and rank is defined
            if _rank == r or rank == None:

                s += "\n"+star+" "+self.name+" "+star+" ["+_rank+"]\n"
                for cat in self.categories:
                    s += "\n\t"+cat+"\n\n"

                    # if the category does not exist for this rank
                    try:
                        self.drops[_rank][cat]
                    except KeyError:
                        log.warning('no ('+cat+') for '+self.name+' '+_rank+'')
                        s+= "\t\tNo data for this category\n"
                        continue
                        

                    for drop in self.drops[_rank][cat]:
                        s+= "\t\t"+drop.show()+"\n"

                result.append(s)
                s = ""

        return result

    # output valid json format
    def __str__(self): 
        
        s = '{\n\tname : \'+self.name+\' '
        result = []

        for _rank in self.ranks:
            s += '{\n\trank :'+_rank+'\n'

            for cat in self.categories:
                s += "\n\t"+cat+"\n\n"

                # if the category does not exist for this rank
                try:
                    self.drops[_rank][cat]
                except KeyError:
                    log.warning('no ('+cat+') for '+self.name+' '+_rank+'')
                    s+= "\t\tNo data for this category\n"
                    continue
                        

                for drop in self.drops[_rank][cat]:
                    s+= "\t\t"+str(drop)+"\n"

        return s

# volatile database
# will hold all the monster data - must be populated first
global_monsters = dict[str, dict[str, Monster]]
mhf1_monsters = dict[str, Monster]
mhfu_monsters = dict[str, Monster]
mhp3_monsters = dict[str, Monster]
mhxx_monsters = dict[str, Monster]

global_monster_names = dict[str, list[str]]
mhf1_monsters_names = [str]
mhfu_monsters_names = [str]
mhp3_monsters_names = [str]
mhxx_monsters_names = [str]

# parse a text file to extract all values and
# create a monster object from it
def text_to_obj(path):

    log.info("processing file "+path)
    errors = []

    file = open(path, encoding="utf_8")
    file.readlines()
    size = file.tell()
    file.seek(0)

    infos = None
    
    # the first line of text should contain the monster name
    while file.tell() < size:

        line = file.readline()
        # if the line contains a star char - ok
        if line.find(star) != -1:
            infos = find_infos(line)
            break
    
    # if no info has been found - exit
    if infos == None:
        log.error('could not find infos in '+path)
        return None

    monster = Monster(infos['monster'], infos['game'])

    current_rank = ""
    current_cat = ""
    current_drop = ""

    
    file.seek(0)

    while file.tell() < size:
        
        #=======================#
        ## MHXX MONSTER SYNTAX ##
        #=======================#
        if infos['game'] == mhxx:

            log.debug('using mhxx layout')

            # skip empty lines
            while line == '\n':
                line = file.readline()

            #check the rank for the next batch of items
            if star in line:
                infos = find_infos(line)
                log.debug("Rank: "+infos['rank'])

            current_rank = infos['rank']
            # check if the rank exists
            check_rank(current_rank)

            #look if there is a line that contains infos about layout
            while line.startswith('Item') == False:
                line = file.readline()
            
            # we can extract infos about the layout here
            log.debug('layout: '+line)
            
            # the next line 'should' contains the items for the current rank
            line = file.readline()
            
            # process and add all rewards for the current category
            while len(line) > 2:
                
                # extract infos from the line
                # item - qty - prob - cat 
                
                # removes the '\n' if any
                line = line.strip('\n')

                # attempts to split the objects
                values = line.split('\t')

                # removes any empty values
                while '' in values:
                    values.remove('')

                log.debug(str(values))
                                    
                # create a drop object
                drop = Drop(values[0], values[2].strip('%'), values[1])
                log.debug(drop)

                # set the drop category
                try:
                    category = values[3]
                except IndexError:
                    log.error('can not add '+values[0]+' for '+monster.name)
                    errors.append(current_rank+' : '+values[0])
                    line = file.readline()
                    continue

                # add to the monster's rewards
                monster.add_drop(current_rank, category, drop)


                # if EOF returns the monster
                if file.tell() == size:
                    file.close()
                
                    # export errors into a file
                    if len(errors) > 0:
                        utils.export_list(errors, '../files/mhxx/'+monster.name+'.txt')
                 
                    return monster
                
                line = file.readline()
            continue
        
        #=========================#
        ## MHFU/MHP3/MHF1 SYNTAX ##
        #=========================#
        drops = []
        
        # skip until we find the line that contains rank
        if line.find(star) == 0:
            infos = find_infos(line)
            log.debug("Rank: "+infos['rank'])

            current_rank = infos['rank']

        # skip until we find the reward type
        while line[0].isnumeric() == False:
            line = file.readline()
            
            # quick n dirty error check
            try:
                line[0]
            except IndexError:
                log.error('cannot process this file')
                return None

        line = line.split( )
        line.remove(line[0])
        reward_type =' '.join(line)
        current_cat = reward_type
        log.debug("  "+reward_type)

        # skip to the next line ( supposedly item )
        while line[0] != '-':
            line = file.readline()
        
        # while the line is an item ( starts with - )
        while len(line) > 2 and line[0] == "-":
            # add the drop into the list
            drop = find_drop_infos(line)
            monster.add_drop(current_rank, current_cat, drop)

            line = file.readline()

        # while the line is a newline
        while len(line) < 3:

            if len(line) == 0:
                drops.clear()
                file.close()
                return monster

            line = file.readline()

        # when the loop reach this point
        # the drops for a specific category is over

    file.close()

# find and process all files found in the given path
# the method 'file_to_obj(file)' is executed for each file found
def files_to_list(path):

    # Looking for monster files
    drop_files = []
    drop_file_type = '.txt'
    drop_files = find_files(path, drop_file_type)
    log.info("Found "+str(len(drop_files))+" drop files")

    # Looking for hitzone files
    hitzone_files = []
    hitzone_file_type = '.stats.json'
    hitzone_files = find_files(path, hitzone_file_type)
    log.info("Found "+str(len(hitzone_files))+" hitzone files")

    monsters = {}
    errors = []
    warnings = []

    # process each drop file
    for f in drop_files:
        
        # check if there is a hitzone file for this monster
        hitzone_file = utils.filetype_exists_for_file(
            f, hitzone_files, drop_file_type, hitzone_file_type)
        
        monster = text_to_obj(f)

        # if the monster is valid - add it
        if monster != None:
            monsters[monster.name] = monster
            # if there is a hitzone file for this monster - add the infos
            if len(hitzone_file) != 0:
                log.debug('hitzone file found for '+monster.game+' '+monster.name)
                monster.stats = parse_monster_stats(hitzone_file)
            else:
                warnings.append('no hitzone file for '
                                +monster.game+' '+monster.name)
                log.warning('no hitzone file for '
                                +monster.game+' '+monster.name)
        else:
            errors.append('Could not process '+f)
            log.error('Could not process '+f)

    log.info(str(len(monsters))+' elements have been added')
    utils.export_list(errors, '../files/.errors.txt')
    utils.export_list(warnings, '../files/.warnings.txt')

    return monsters

def parse_monster_stats(stats_file: str):
    'parse all the hitzone values and other stats from a .json file'

    file = open(stats_file, encoding="UTF_8")

    json_data: dict = json.loads(file.read())
    _parts = json_data['hitzone']

    stats = Stats()

    # parts creation
    for part_name in _parts:
        _part = _parts[part_name]

        part = Part(part_name.lower().replace('_',' '))
        part.stagger = _part['stagger']
        
        # loop through each 'mode' the monster has for this part
        for mode_name in _part:
            _values = _part[mode_name]
            
            # skip non array values such as stagger value
            if type(_values) is not list:
                continue
            
            if mode_name not in stats.modes:
                stats.modes.append(mode_name)
            
            hitzone_values = HitzoneValues(mode_name)

            # if not enough values for each type of damange
            if len(_values) < 8:
                log.warning('hitzone ' + 'MONSTER ' + mode_name + part_name)
                log.warning('   one or more damage type value missing')
                
                # add dummy values
                while len(_values) < 8:
                    _values.append('ERR')

            hitzone_values.cut      = _values[0]
            hitzone_values.impact   = _values[1]
            hitzone_values.shot     = _values[2]
            hitzone_values.fire     = _values[3]
            hitzone_values.water    = _values[4]
            hitzone_values.thunder  = _values[5]
            hitzone_values.dragon   = _values[6]
            hitzone_values.ice      = _values[7]

            part.hitzone_values.append(hitzone_values)

        stats.parts.append(part)

    # rage mode defense multiplier
    if 'rage_m' in json_data.keys():
        stats.rage_multiplier = json_data['rage_m']
    else:
        stats.rage_multiplier = 0.0

    # get notes
    for mode in stats.modes:
        key = 'notes_'+mode
        if key in json_data.keys():
            stats.notes[mode] = json_data[key]

    if 'notes' in json_data.keys():
        stats.notes['all'] = json_data['notes']
    
    return stats

def obj_to_json(monster):

    # pretty printing
    return json.dumps(monster.drops, sort_keys=True, indent=4)

def create_monster_list(monsters):

    name_list = []
    # retreive monster names 
    for key in monsters.keys():
        name_list.append(key)

    return name_list

# string related functions

# this method must extract
#   item name
#   qty
#   drop rate
#
def find_drop_infos(line):

    item_name = ""
    item_qty = 1
    drop_rate = 0

    line = line.split( )
    
    # removes the '-' if there is one
    if line[0] == '-':
        line.remove(line[0])

    # we must find how many words the name has
    for word in line:

        if word[0] == "x":
        # QUANTITY

            item_qty = int(word[1:])
            log.debug("\tquantity: "+str(item_qty))

        elif word.find("%") != -1:
        # DROP RATE

            # if the value is in between parenthesis
            if word.startswith('('):
                word = word[1:len(word)-1]

            drop_rate = int(word[:len(word)-1])
            log.debug("\tdrop rate: "+str(drop_rate)+"%")

        else:
        # ITEM NAME
            log.debug("\tname: "+word)
            item_name = item_name+" "+word

    item_name = item_name[1:]
    drop = Drop(item_name, drop_rate, item_qty)
    log.debug(drop)
    return drop

def find_infos(line):

    log.info("looking for monster infos")
    l = line.split( )
    log.debug(l)
    i = 0
    name = ""
    rank = None
    game = ""
    is_name = True

    # removes any leading special characters
    if '\ufeff' in l[0]:
        log.debug('removed special character')
        l = l[1:]

    # check each word in the line
    while i < len(l):

        # if its the star - skip
        if l[i] == star or l[i] == '-':
            log.debug('skipping value: '+l[i])
            i = i+1
            continue
        else:
            
            word = l[i].lower()
            # determine the rank
            if rank == None:
                rank = check_rank(word)

            # determine the game
            if game == "":
                # check if the word is one of em - if true - skip
                if word in wordlist_fu:
                    game = mhfu
                elif word in wordlist_p3:
                    game = mhp3
                elif word in wordlist_f1:
                    game = mhf1
                elif word in wordlist_xx:
                    game = mhxx
                if game != "":
                    log.debug("game: "+game)

            if is_name and (rank != None or len(game) > 0):
                is_name = False
                    
            if is_name:
                name = name+" "+l[i]
        i = i+1
    if rank == None:
        log.warning('no rank found for '+name)
        log.warning(line)
        rank = 'undefined'
        
    log.debug('name: '+name)
    log.info('\t'+name[1:]+' - '+game+' '+rank)
    return {"monster": name[1:], "game": game, "rank": rank}


# method to search a specific item into the given list
def find_item(monster_list, item_name, as_list=False):

    ml = monster_list
    name = item_name

    results = ""
    results_list = []
    for m in ml.values():

        found = m.find_item(name)

        if len(found) > 0:
            results_list += ["\n\n"+m.name+found]
            results = results+"\n\n"+m.name
            results = results+found

    if len(results) == 0:
        results = "No result found."
        results_list += [results]

    if as_list == True:
        return results_list
    else:
        return results

def find_files(path, filetype=''):

    files = []
    log.debug('looking for '+filetype+' files into '+path)
    for f in os.scandir(path):
        if f.is_file() and f.name.endswith(filetype):
            files.append(f.path)
            log.debug('FILE FOUND: '+f.path)
        elif f.is_dir(): 
            files = files + find_files(f.path, filetype)

    return files


# find all existing items from the monsterlist
# return list that contains item names only
def find_items(monster_list):

    items = []
    mons = []
    v = []

    for m in monster_list.values():

        for rank in m.ranks:
            for cat in m.categories:

                # if the category does not exist for this rank
                try:
                    m.drops[rank][cat]
                except KeyError:
                    log.warning('no ('+cat+') for '+m.name+' '+rank+'')
                    continue

                for drop in m.drops[rank][cat]:

 
                    if drop.name not in items:
                        mons.append(m.name)
                        items.append(drop.name)

                        v.append(drop.name+" - "+m.name+",")
                        log.debug("(ADDED) - "+drop.name+" : "+m.name)

                    else:
                        i = items.index(drop.name)

                        if m.name+"," not in v[i]:
                            v[i] = v[i]+" "+m.name+","

                        log.debug("(NOT-ADDED) - "+drop.name+" : "+m.name)

    v.sort()
    items.sort()

    for i in range(len(mons)):
        log.debug(items[i])

    return items
     
# search an item from all the existing monsters in the list
# 'name' can be the ID of the item previously shown by this method
# 
# search_item(str, dict):
#     return str
#
def search_item(name, monster_list):

    # find all the possible items first
    item_list = find_items(monster_list)

    results = []
    # if name is the ID - check and return the item
    try:
        item_id = int(name)
    except ValueError:
        log.debug(name+" is not an ID")
    else:
        # if the ID does exist
        try:
            results += ['['+str(item_id)+'] '+item_list[item_id]]
            result = find_item(monster_list,item_list[item_id])
            # if the message will be too long - split it
            if len(result) > 1800:
                results += find_item(monster_list,item_list[item_id],as_list=True)
            else:
                results += [result]
            return results
        except IndexError:
            return ["Incorrect Item ID"]

    # search if the name matches with any item
    matches = utils.search(name, item_list) 
    matches_s = len(matches)

    # if nothing match
    if matches_s == 0:
        return ["Nothing found"]

    # if exaclty 1 match is found
    if matches_s == 1:
        results += ['['+str(item_list.index(matches[0]))+'] '+matches[0]]
        result = find_item(monster_list,matches[0])
        # if the message will be too long - split it
        if len(result) > 1800:
            results += find_item(monster_list,matches[0],as_list=True)
        else:
            results += [result]
        return results

    # if multiples match are found
    if matches_s > 1:
        r = ""
        for match in matches:
            r += '['+str(item_list.index(match))+'] '+match+'\n'
        return [r]

# search for a monster in a list
# return list containing matching names if any
def search_monster_2(name, monsters):
    # if name is empty
    if name.strip() == '' or name == None:
        return -2

    name_list = []
    results = []

    # retreive monster names 
    for key in monsters.keys():
        name_list.append(key)
    
    args = name.split()
    last_arg = args.pop().upper()
    rank = None
    # check if there is a rank suffix inside the name
    if last_arg in rank_suffix.keys():
        rank = rank_suffix[last_arg]
        print('found rank '+rank)
    else:
        args.append(last_arg)
    
    name = ' '.join(args)
    log.debug('now searching for '+name)

    # if name is the ID - check and return the monster
    try:
        name_id = int(name)
    except ValueError:
        log.debug(name+' is not an ID')
    else:
        # if the ID does exist
        try:
            results.append(name_list[name_id])
            #results += ['['+str(name_id)+'] '+name_list[name_id]]
            #results += monster_list[name_list[name_id]].show(rank=rank)
            return results
        except IndexError:
            # incorrect ID
            return -1

    # search if the name matches with any item
    matches = utils.search(name, name_list) 
    matches_s = len(matches)

    # if nothing match
    if matches_s == 0:
        return results

    # if exaclty 1 match is found
    if matches_s == 1:
        #results += ['['+str(name_list.index(matches[0]))+'] '+matches[0]]
        #results += monster_list[matches[0]].show(rank=rank)
        results.append(matches[0])
        return results

    # if multiples match are found
    if matches_s > 1:
        for match in matches:
            #results.append(match)
            results.append('['+str(name_list.index(match))+'] '+match)
        return results
    


class ResultCode:

    UNDEFINED = -1
    NO_SUCH_ID = 10
    NOTHING_FOUND = 11
    MISSING_ARG = 12
    FOUND_MANY = 13
    FOUND_DATA = 14
    NO_DATA = 15

class SearchResult:

    def __init__(self, code: int = ResultCode.UNDEFINED) -> None:
        self.code: int = code
        self.message: str
        self.description: str
        self.content: any

class HitzoneContent:
        
    def __init__(self) -> None:
        self.mode: str
        self.header: str
        self.table: str
        self.footer: str
        self.notes: str

class HitzoneSearchResult(SearchResult):

    def __init__(self, code: int = ResultCode.UNDEFINED) -> None:
        super().__init__(code)
        self.monster: Monster
        self.content: list[HitzoneContent] = []

def search_hitzone_data(monster_name: str, 
                  monsters: dict[str, Monster], 
                  monster_list: list) -> HitzoneSearchResult:
    '''
    Searches into an exisiting monster list for hitzone data.
    Requires a monster and a monster names list
    '''

    result = HitzoneSearchResult()
    search_result = search_monster_2(monster_name, monsters)

    # if the result is an error
    if type(search_result) is int:

        if search_result == -1:
            result.code = ResultCode.NO_SUCH_ID
            result.message = 'Incorrect monster ID'
        elif search_result == -2:
            result.code = ResultCode.MISSING_ARG
            result.message = 'Missing monster name or ID'
        elif search_result < 0:
            result.code = ResultCode.UNDEFINED
            result.message = 'Undefined Error '+str(search_result)
        return result

    # if the result contain no error
    if type(search_result) is list:

        # nothing found
        if len(search_result) == 0:
            result.code = ResultCode.NOTHING_FOUND
            result.message = 'No monster found'
            return result
        # multiple results
        elif len(search_result) > 1:
            result.code = ResultCode.FOUND_MANY
            result.message = 'Multiple monsters found'
            result.content = ''
            for element in search_result:
                result.content += str(element)+'\n'
            return result
        
        
        log.debug('Found 1 monster')
        monster: Monster = monsters.get(search_result[0])
        result.monster = monster
        message = '['+str(monster_list.index(monster.name))+'] '+monster.name

        if monster.stats == None:
            result.code = ResultCode.NO_DATA
            result.message = 'No hitzone data for '+monster.name
            return result
        else:
            result.code = ResultCode.FOUND_DATA
            result.message = message

            # generate hitzone text data for each mode
            
            for mode in monster.stats.modes:
                hitzone_content = HitzoneContent()
                hitzone_content.mode = mode

                mode_id = monster.stats.modes.index(mode)

                hitzone_td = build_hitzone_table_data(monster.stats, mode_id)
                hitzone_t = build_hitzone_table(hitzone_td)
                hitzone_content.table = hitzone_t

                hitzone_content.header = '['+monster.game.upper()+'] Hitzone Data  :  '+monster.name+' - '+mode.title()

                hitzone_content.footer = 'Rage Defense Multiplier: '+str(monster.stats.rage_multiplier)+'\n'

                hitzone_content.notes = ''
                
                if monster.stats.notes.get('all'):
                    hitzone_content.footer += ''+monster.stats.notes['all']+'\n'
                    hitzone_content.notes = ''+monster.stats.notes['all']+'\n'
                if monster.stats.notes.get(mode):
                    hitzone_content.footer += ''+monster.stats.notes[mode]+'\n'
                    hitzone_content.notes += ''+monster.stats.notes[mode]+'\n'

                result.content.append(hitzone_content)

        return result

    return result

# returns a list
def search_monster(name, monster_list, rank=None):
    
    # if name is empty
    if name == '' or name == None:
        return ['Missing name or ID']

    name_list = []
    results = []

    # retreive monster names 
    for key in monster_list.keys():
        name_list.append(key)
    
    args = name.split()
    last_arg = args.pop().upper()
    rank = None
    # check if there is a rank suffix inside the name
    if last_arg in rank_suffix.keys():
        rank = rank_suffix[last_arg]
        print('found rank '+rank)
    else:
        args.append(last_arg)
    
    name = ' '.join(args)
    log.debug('now searching for '+name)

    # if name is the ID - check and return the monster
    try:
        name_id = int(name)
    except ValueError:
        log.debug(name+' is not an ID')
    else:
        # if the ID does exist
        try:
            results += ['['+str(name_id)+'] '+name_list[name_id]]
            results += monster_list[name_list[name_id]].show(rank=rank)
            return results
        except IndexError:
            return ['Incorrect Monster ID']

    # search if the name matches with any item
    matches = utils.search(name, name_list) 
    matches_s = len(matches)

    # if nothing match
    if matches_s == 0:
        return ['Nothing found']

    # if exaclty 1 match is found
    if matches_s == 1:
        results += ['['+str(name_list.index(matches[0]))+'] '+matches[0]]
        results += monster_list[matches[0]].show(rank=rank)
        return results

    # if multiples match are found
    if matches_s > 1:
        r = ''
        for match in matches:
            r += '['+str(name_list.index(match))+'] '+match+'\n'
        return [r]

# display various information such as
# ranks ( monster appearances )
# rewards catgories
#
def show_m_categories(monster_list):

    for m in monster_list.values():
        print("ranks for "+m.name)
        for rank in m.ranks:
            print("  "+rank)

        print("categories for "+m.name)
        for cat in m.categories:
            print("  "+cat)

# generate a list that contains all items along with the
# associated monsters
def generate_itemlist(monster_list):

    items = {}

    for m in monster_list.values():
        for r in m.ranks:
            for c in m.categories:

                # if the category does not exist for this rank
                try:
                    m.drops[r][c]
                except KeyError:
                    log.warning('no ('+c+') for '+m.name+' '+r+'')
                    continue

                for drop in m.drops[r][c]:

                    if drop.name not in items.keys():
                        items[drop.name] = m.name+', '
                    else:
                        names = items[drop.name].split(', ')

                        if m.name not in names:
                            items[drop.name] += m.name+', '

    results = {}
    for key in sorted(items.keys()):
        results[key] = items[key]
    
    return results

    #for item in items.keys():
    #    results.append(item+" : "+items[item])
    #    results.sort()
    

    
    #return {'list': results, 'items': items.keys()}

# performs a deep check
#
# dict monsters  - monster list
# dict items     - original item names list
#
# return ?
#
def check_monsters(monsters, items=None):
    log.info('checking monster infos')
    
    issues = []
    # item name verification
    if items != None:
        
        # generates an itemlist from the monsters
        log.info('generating itemlist from monsters')
        m_items = generate_itemlist(monsters)
        
        issues.append('ITEM NAMES ISSUES :\n')
        for item in m_items.keys():
            
            # if the item does not exist in the list
            if item not in items:
                log.warning(item+' not found')
                issues.append('\t'+item+' : '+m_items[item])

    return issues


def build_hitzone_table_data(stats, monster_mode=0, padding=0):
    'monster mode refers to normal, rage, etc'

        
    default_value = ''

    headers = []
    headers.append('PART')
    headers.append(' ')
    headers.append(dmg_type_cut)
    headers.append(dmg_type_impact)
    headers.append(dmg_type_shot)
    headers.append('')
    headers.append(dmg_type_fire)
    headers.append(dmg_type_water)
    headers.append(dmg_type_thunder)
    headers.append(dmg_type_ice)
    headers.append(dmg_type_dragon)
    headers.append('')
    headers.append(dmg_stagger)

    columns = len(headers)
    rows = len(stats.parts) + 1

    table_data = [[default_value] * columns for i in range(rows)]
    table_data = []

    table_data.append(headers)

    part: Part
    for part in stats.parts:

        values: HitzoneValues = part.hitzone_values[monster_mode]
        line = []
        line.append(part.name.title())
        line.append('')
        line.append(values.cut)
        line.append(values.impact)
        line.append(values.shot)
        line.append('')
        line.append(values.fire)
        line.append(values.water)
        line.append(values.thunder)
        line.append(values.dragon)
        line.append(values.ice)
        line.append('')
        line.append(part.stagger)

        table_data.append(line)

    return table_data

def build_hitzone_table(table_data):
    tbl_d = txtutils.slim_tbl_d
    col_sizes = [8, 0, 4, 4, 4, 0, 3, 3, 3, 3, 3, 0, 5]
    hitzone_table = txtutils.text_table(
        table_data, column_sizes=col_sizes, padding=1, table_delimiters=tbl_d)
    return hitzone_table

def get_hitzone_image(hitzone_data: HitzoneContent) -> str:

    root_path = '../.tests/'
    img_path = root_path+'/img/test.png'
    fnt_path = root_path+'fonts/UbuntuMono-Bold.ttf'
    text_data = ''
    text_data += hitzone_data.header+'\n'
    text_data += hitzone_data.table
    # text_data += hitzone_data.footer
    txtutils.text_to_image(text_data, image_path=img_path, font_path=fnt_path, padding=15)
    return img_path