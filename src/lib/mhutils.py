import os
import json
import logging as log

import lib.utils as utils

files_path = '../files'
mhfu_path = files_path+'/mhfu'
star = "☆"

# used for JSON values
star_1_2 = "1-2 Star"
low_rank = "Low-Rank"
high_rank = "High-Rank"
g_rank = "G-Rank"

mhp3 = "MHP3"
mhfu = "MHFU"

rank_suffix = {
    '1-2': star_1_2,
    'LR' : low_rank,
    'HR' : high_rank,
    'G'  : g_rank,
}
_rank_suffix = ['1-2','LR','HR','G']


wordlist_12 = ["1-2","1/2", '1-2 star']
wordlist_lr = ["village","village/low","village/low-rank","low","low-rank","lr"]
wordlist_hr = ["high","hr","high-rank"]
wordlist_g = ["g","g-rank"]
wordlist_p3 = ["p3","mhp3"]
wordlist_fu = ["fu","mhfu"]


wordlist_rank = wordlist_12+wordlist_lr+wordlist_hr+wordlist_g
wordlist_game = wordlist_fu+wordlist_p3

log.basicConfig(level='WARNING')

# check the term and return the rank if it does match any
def check_rank(terms): 
    
    log.info('checking rank: '+str(terms))
    if terms == None:
        return
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
    else:
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


class Monster:
    'Defines monster structure'

    def __init__(self, name, game):
        self.name = name
        self.game = game

        # contains all rank appearances
        self.ranks = []
        # contains all drop categories
        self.categories = []
        # contains all drops for a category
        self.drops = {}

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
           add_drop(self, rank, category, drop)

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
    def get_drops(rank):
        
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

# parse a text file to extract all values and
# create a monster object from it

def text_to_obj(path):

    log.info("processing file "+path)

    file = open(path)
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
        
        drops = []
        
        # skip until we find the line that contains rank
        if line.find(star) == 0:
            infos = find_infos(line)
            log.debug("Rank: "+infos['rank'])

            current_rank = infos['rank'] 

        # skip until we find the reward type
        while line[0].isnumeric() == False:
            line = file.readline()
    
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
    files = []
    
    files = find_files(path)
    log.info("Found "+str(len(files))+" files")

    monsters = {}

    # process each file
    for f in files:

        monster = text_to_obj(f)

        # if the monster is valid - add it
        if monster != None:
            monsters[monster.name] = monster

    log.info(str(len(monsters))+' elements have been added')

    return monsters

def obj_to_json(monster):

    # pretty printing
    return json.dumps(monster.drops, sort_keys=True, indent=4)


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
    rank = ""
    game = ""
    is_name = True

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
            if rank == "":
                # check if the word is one of em - if true - skip
                if word in wordlist_12:
                    rank = star_1_2
                elif word in wordlist_lr:
                    rank = low_rank
                elif word in wordlist_hr:
                    rank = high_rank
                elif word in wordlist_g:
                    rank = g_rank
                if rank != "":
                    log.debug("rank: "+rank)

            # determine the game
            if game == "":
                # check if the word is one of em - if true - skip
                if word in wordlist_fu:
                    game = mhfu
                elif word in wordlist_p3:
                    game = mhp3
                if game != "":
                    log.debug("game: "+game)

            if is_name and (len(rank) > 0 or len(game) > 0):
                is_name = False
                    
            if is_name:
                name = name+" "+l[i]
        i = i+1

    log.info('\t'+name[1:]+' - '+game+' '+rank)
    return {"monster": name[1:], "game": game, "rank": rank}


# method to search a specific item into the given list
def find_item(monster_list, item_name):

    ml = monster_list
    name = item_name

    results = ""
    for m in ml.values():

        found = m.find_item(name)

        if len(found) > 0:
            results = results+"\n\n"+m.name
            results = results+found
    if len(results) == 0:
        results = "No result found."

    return results

def find_files(path):

    files = []
    log.info('looking for files into '+path)
    for f in os.scandir(path):
        if f.is_file():
            files.append(f.path)
            log.info('FOUND: '+f.path)
        elif f.is_dir(): 
            files = files + find_files(f.path)

    return files

    print("Results for "+item+" : "+results)


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

    results = ""
    # if name is the ID - check and return the item
    try:
        item_id = int(name)
    except ValueError:
        log.debug(name+" is not an ID")
    else:
        # if the ID does exist
        try:
            results = ['['+str(item_id)+'] '+item_list[item_id]]
            results.append(find_item(monster_list,item_list[item_id]))
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
        results = ['['+str(item_list.index(matches[0]))+'] '+matches[0]]
        results.append(find_item(monster_list,matches[0]))
        return results

    # if multiples match are found
    if matches_s > 1:
        r = ""
        for match in matches:
            r += '['+str(item_list.index(match))+'] '+match+'\n'
        return [r]

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
