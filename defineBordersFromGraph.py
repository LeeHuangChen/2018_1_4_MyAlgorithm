import os
from cPickle import dump,load, HIGHEST_PROTOCOL
import networkx as nx
import configurations as conf
import util

#borders is a list of list consists of elements: [ModuleID,start,end]
#this returns true if there is a border that intersects with another border in borders
def containsOverlapBorders(borders):
	for i in range(len(borders)):
		for j in range(i+1,len(borders)):
			if (borders[i][0]==borders[j][0]):
				overlapped=util.overlap(borders[i][1],borders[i][2],borders[j][1],borders[j][2])>0
				if overlapped:
					return (i,j)
	return False

def collapsOverlappingBorders(borders):
	overlapInfo=containsOverlapBorders(borders)
	while(overlapInfo!=False):
		i=overlapInfo[0]
		j=overlapInfo[1]
		border1=borders[i]
		border2=borders[j]
		newstart=min(border1[1],border2[1])
		newend=max(border1[2],border2[2])
		#newborder=[border1[0],newstart,newend]

		#delete the overlapped border and add the merged border
		deleteindex=None
		otherindex=None
		if i>j:
			deleteindex=i
			otherindex=j
		else:
			deleteindex=j
			otherindex=i
		
		del borders[deleteindex]

		borders[otherindex][1]=newstart
		borders[otherindex][2]=newend
		#border.append(newborder)

		overlapInfo=containsOverlapBorders(borders)
		


def defineBordersFromGraph(graphFile, hspIntGraphdir, borderInfodir, borderResultdir):
	#generate the directories
	util.generateDirectories(borderInfodir)
	util.generateDirectories(borderResultdir)


	with open(os.path.join(hspIntGraphdir,graphFile)) as fin:
		g=load(fin)

	#find the connected components of the graph:
	CCgraphs = list(nx.connected_component_subgraphs(g))
	CCgraphs.sort(key=lambda tup:len(tup.nodes()))

	#create a dictionary where key=protein name, val:border information
	modulefamilyinfo={}
	for moduleID, CCgraph in enumerate(CCgraphs):
		for node in CCgraph.nodes():
			
			proteinName=node[0]
			start=int(node[1])
			end=int(node[2])

			if(proteinName not in modulefamilyinfo):
				modulefamilyinfo[proteinName]=[[moduleID,start,end]]
			else:
				#if we already have information on this protein
				modulefamilyinfo[proteinName].append([moduleID,start,end])
				collapsOverlappingBorders(modulefamilyinfo[proteinName])

				##testcode
				# for protein in modulefamilyinfo.keys():
				# 	print protein, modulefamilyinfo[protein]
				# print "**"
				# print [moduleID,start,end]
				# raw_input("Press Enter to continue...")


				# borders=modulefamilyinfo[proteinName]

				# weShouldAddABorder=True
				# for border in borders:
				# 	#if there is a border in the module information that overlaps with the current border and it is from the same module family
				# 	overlapped=util.overlap(border[1],border[2],start,end)>0
				# 	if overlapped and border[0]==moduleID:
				# 		#then replace the border with the union of the borders
				# 		border[1]=min(border[1],start)
				# 		border[2]=max(border[2],end)
				# 		weShouldAddABorder=False

				# if weShouldAddABorder:
				# 	modulefamilyinfo[proteinName].append([moduleID,start,end])
				# 	collapsOverlappingBorders(modulefamilyinfo[proteinName])

	#cleanup borders that ended up developing to overlap borders
	for protein in modulefamilyinfo.keys():
		collapsOverlappingBorders(modulefamilyinfo[protein])

	#save the border information dataset
	with open(os.path.join(borderInfodir, graphFile.replace('_HSPIntGraph.gpickle',"")+'_BorderInformation.gpickle'),'wb') as fout:
		moduleNumInfo=("Number of modules detected",len(CCgraphs))
		familyInfoWrap=("ModuleFamilyInfo, Format: Dict\{proteinName, list[borders[moduleId,start,end]] \}", modulefamilyinfo)
		dump((moduleNumInfo,familyInfoWrap), fout, HIGHEST_PROTOCOL)


	#write the information down in a text file.
	resultFile=open(os.path.join(borderResultdir,graphFile.replace('_HSPIntGraph.gpickle',"")+'_ModuleInfo.txt'),"w")
	resultFile.write("Number of modules detected: "+str(len(CCgraphs))+"\n\n")
	resultFile.write("proteinName\t borders\n")
	proteins = modulefamilyinfo.keys()
	proteins.sort()

	for protein in proteins:
		resultFile.write(protein)
		borders=modulefamilyinfo[protein]
		for border in borders:
			moduleID=border[0]
			start=border[1]
			end=border[2]
			resultFile.write("\tM_"+str(moduleID)+"("+str(start)+","+str(end)+")")
		resultFile.write("\n")
	resultFile.close()

	return 0


def main(graphFile):
	hspIntGraphdir=conf.hspIntGraphdir
	borderInfodir=conf.borderInfodir
	borderResultdir=conf.borderResultdir
	defineBordersFromGraph(graphFile, hspIntGraphdir, borderInfodir,borderResultdir)
	return 0
