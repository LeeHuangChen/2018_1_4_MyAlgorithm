import os, re
from cPickle import dump,load, HIGHEST_PROTOCOL
import networkx as nx
import configurations as conf
import util
import sys



        

#, query, target, query_start, query_end, target_start, target_end, align_length, identity):
# reads the relevant information from a line of the all-to-all from BLASTp the format of the result is shown below:
    #[0    , 1      , 2  , 3       , 4       , 5      , 6  , 7   , 8  , 9   , 10    , 11]
    # query, subject, %id, alignlen, mismatch, gapopen, qst, qend, sst, send, Evalue, bitscore
def read_HSP(line):
    splitArray=line.split("\t")
    hsp = {}
    hsp["query_id"] = splitArray[0]
    hsp["target_id"] = splitArray[1]

    hsp["query_start"]=  int(splitArray[6])
    hsp["query_end"] = int(splitArray[7])
    hsp["query_len"]= hsp["query_end"]-hsp["query_start"]

    hsp["target_start"]= int(splitArray[8])
    hsp["target_end"] = int(splitArray[9])
    hsp["target_len"] = hsp["target_end"]-hsp["target_start"]

    hsp["EValue"] = float(splitArray[10])
    
    return hsp

def nodeName(hsp, focus):
    name=""
    if focus=="target":
        name=(hsp["target_id"],str(hsp["target_start"]),str(hsp["target_end"]))
    elif focus == "query":
        name=hsp["query_id"],str(hsp["query_start"]),str(hsp["query_end"])
    return name



#looks at the four intervals provided by the two hsp (each hsp has two intervals in the form (q,s,e), (t,s,e)), and returns a list of nodeName pairs to add edges
def findOverlapIntervals(name1, name2, cutoffRatio):
    nodeNamePairs=[]

    interval1Start=int(name1[1])
    interval1End=int(name1[2])
    interval2Start=int(name2[1])
    interval2End=int(name2[2])

    overlap=util.overlap(interval1Start,interval1End,interval2Start,interval2End)
    intervalLen1=interval1End-interval1Start 
    intervalLen2=interval2End-interval2Start

    overlapRatio1=float(overlap)/float(intervalLen1)
    overlapRatio2=float(overlap)/float(intervalLen2)

    maxOverlapRatio=max(overlapRatio1, overlapRatio2)

    if(name1[0]!=name2[0]):
        print "Error!!! ", name1, name2

    #add the nodeNamePair to nodeNamePairs
    if maxOverlapRatio>cutoffRatio:
        #print name1,name2
        nodeNamePairs.append(   (name1,name2)   )
                
    return nodeNamePairs

def addToDict(dictionary, key, append):
    if key in dictionary:
        #add the element to list and remove duplicates
        #print dictionary
        #print append
        dictionary[key].append(append)
        dictionary[key]=list(set(dictionary[key]))
    else:
        dictionary[key]=[append]

def build_graph(blastInfoFilename,blastdir, hspIntGraphdir, cutoffRatio, evalueCutoff):
    
    #Generate the output folder
    util.generateDirectories(hspIntGraphdir)

    g=nx.Graph()

    
    #read the file
    f=open(os.path.join(blastdir,blastInfoFilename),"r")
    content=f.read()
    f.close()

    #a dictionary that stores node names by the protein names
    nodeNames={}

    #add the HSP edges
    for i, line in enumerate(content.split("\n")):
        if(i%(len(content.split("\n"))/10)==0):
            #sys.stdout.write(str(int(float(10*i)/float(len(content.split("\n"))))))
            sys.stdout.write("*")
            sys.stdout.flush()
        if len(line)>0:
            hsp=read_HSP(line)
            goodeval=hsp["EValue"]<evalueCutoff
            notsameprotein = (hsp["query_id"]!=hsp["target_id"])
            if goodeval and notsameprotein:

                #Add the nodes (p_1,s_1,e_1) and (p_2,s_2,e_2) and create an edge between them
                g.add_node(nodeName(hsp,"query"))
                g.add_node(nodeName(hsp,"target"))
                g.add_edge(nodeName(hsp,"query"),nodeName(hsp,"target"), eValue=hsp["EValue"])

                #add the two node names to the nodeNames dictionary and take away the duplicates
                addToDict(nodeNames,nodeName(hsp,"query")[0],nodeName(hsp,"query"))
                addToDict(nodeNames,nodeName(hsp,"target")[0],nodeName(hsp,"target"))

    sys.stdout.write("\n")
    sys.stdout.flush()

    #add the Interval edges
    proteins=nodeNames.keys()
    for protein in proteins:
        # if(i%(len(proteins)/10)==0):
        #     sys.stdout.write("*")
        #     sys.stdout.flush()
        subNodeNames=nodeNames[protein]
        for i in xrange(len(subNodeNames)-1):
            for j in xrange(i+1, len(subNodeNames)):
                name1 = subNodeNames[i]
                name2 = subNodeNames[j]
                

                overlapPairs=findOverlapIntervals(name1, name2, cutoffRatio)
                
                for overlapPair in overlapPairs:
                    g.add_edge(overlapPair[0],overlapPair[1])
    # sys.stdout.write("\n")
    # sys.stdout.flush()


    #save the HSPIntGraph
    splitFilename=blastInfoFilename.split(".")
    fileExt="."+splitFilename[len(splitFilename)-1]
    outputFile=blastInfoFilename.replace(fileExt,"")+'_HSPIntGraph.gpickle'
    outputPath=os.path.join(hspIntGraphdir, outputFile)
    with open(outputPath,'wb') as fout:
        dump(g, fout, HIGHEST_PROTOCOL)
    
    return outputFile

def main(blastInfoFilename):
    #blastdir=conf.blastdir
    hspIntGraphdir=conf.hspIntGraphdir
    cutoffRatio=conf.cutoffRatio
    evalueCutoff=conf.evalueCutoff
    blastdir=conf.blastdir
    return build_graph(blastInfoFilename,blastdir, hspIntGraphdir, cutoffRatio, evalueCutoff)



