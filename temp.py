import os

inputFolder="InputFiles/BLASTp_AllToAll_Data/"
resultsFolder="Results"


for resultFile in os.listdir(resultsFolder):
	corrFile=resultFile.replace("_ModuleInfo.txt",".csv")
	corrPath=os.path.join(inputFolder,corrFile)
	if os.path.exists(corrPath):
		os.rename(corrPath, corrPath.replace(".csv", ".csv.done"))