import configurations as conf
import build_HSPInt_graph as buildintgraph
import defineBordersFromGraph
import os



def main():

	blastdir=conf.blastdir
	blastInfoFilenames=os.listdir(blastdir)
	#go through every file entered in the "InputFiles/BLASTp_AllToAll_Data" directory
	for i, blastInfoFilename in enumerate(blastInfoFilenames):
		print "processing",blastInfoFilename,"(", int(100*float(i)/float(len(blastInfoFilenames))),"% )"
		graphFile=buildintgraph.main(blastInfoFilename)
		defineBordersFromGraph.main(graphFile)

		blastInfoPath=os.path.join(blastdir ,blastInfoFilename)
		os.rename(blastInfoPath,blastInfoPath+".done")


	f=open("TASKCOMPLETED.txt","w")
	f.close()


if __name__ == '__main__':
    main()