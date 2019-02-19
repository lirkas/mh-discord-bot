import os
import logging as log


# search one or more terms into a list
# and returns the matches
# 
# search(str, list):
#    return list
#
def search(terms, _list):
    
    # try to find a matching result from the given terms
    log.info("looking for "+terms)
    
    results = []
    
    # first check if the terms exactly matches with a name
    for value in _list:
        
        # if the terms exactly match with any of the values - return the value
        if value.lower() == terms.lower():

            log.info("found a match for "+value)
            results.append(value)
            return results

    # a dict that will record each match and its pertinance
    # res['item'] = 'item name'
    # res['matches'] = 3
    res = {}
    max_matches = 0

    # check each term individually
    for value in _list:
        
        res[value] = 0

        for term in terms.split( ):
            for word in value.split( ):
                
                if term.lower() == word.lower():
                    res[value] += 1
                    continue

                elif term.lower() in word.lower():
                    res[value] += 1
                    continue

        # update the mex_terms record
        if res[value] > max_matches:
            max_matches = res[value]
            log.debug("max_matches updated to "+str(res[value]))
    
    # if max_matches == 0 ( nothing found ) - stop here
    if max_matches == 0:
        return results

    # add only the value that match the most
    for value in res.keys():
        
        # if the match is good enough - add it
        if res[value] == max_matches:
            results.append(value)

    return results

# import a list from a file
def import_list(path):

    # if the file does no exist - return
    try:
        f = open(path, 'r')
    except FileNotFoundError:
        log.error('file '+path+' not found')
        return None

    _list = []
    size = os.path.getsize(path)

    for line in f:
        _list.append(line[:len(line)-1])

    f.close()
    return _list

# export a list into a file
def export_list(_list, path):

    f = open(path, 'w')
    for e in _list:
        f.write(str(e)+'\n')
    f.close()
