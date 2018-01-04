import os
#A module that contains a number of utility function used across different files

def overlap(s1start, s1end, s2start, s2end):
    maxstart = max(s1start, s2start)
    minend = min(s1end, s2end)
    if maxstart < minend:
        return minend - maxstart
    else:
        return 0


#generate all the directories needed for the given path (helper function)
def generateDirectories(path):
    folders=path.split("/")
    curdir=""
    for folder in folders:
        curdir=os.path.join(curdir,folder)
        if not os.path.exists(curdir):
            os.mkdir(curdir)