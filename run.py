import configurations as conf
import build_HSPInt_graph as buildintgraph
import defineBordersFromGraph
import os
import time



def main():

	blastdir=conf.blastdir
	blastInfoFilenames=os.listdir(blastdir)
	blastInfoFilenames.sort()
	#go through every file entered in the "InputFiles/BLASTp_AllToAll_Data" directory
	#it will mark all the files with '.done' after it is completed
	#this is to ensure that you can restart the experiment and not have to redo the test you have done already
	for i, blastInfoFilename in enumerate(blastInfoFilenames):
		if ".done" not in blastInfoFilename:
			print "processing",blastInfoFilename,"(", int(100*float(i)/float(len(blastInfoFilenames))),"% )"
			#start timer
			startTime=time.time()
			#define the graphs
			graphFile=buildintgraph.main(blastInfoFilename)
			#define the borders from the graphs
			defineBordersFromGraph.main(graphFile)
			#stop the timer
			stopTime=time.time()
			timeDiff=stopTime-startTime

			print "completed in ",timeDiff, "seconds"


			blastInfoPath=os.path.join(blastdir ,blastInfoFilename)
			os.rename(blastInfoPath,blastInfoPath+".done")



	#f=open("TASKCOMPLETED.txt","w")
	#f.close()


if __name__ == '__main__':
	main()