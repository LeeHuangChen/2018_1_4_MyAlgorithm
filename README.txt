#############################
# INSTALLATION INSTRUCTIONS #
#############################
To run this program, first you need to run an all-to-all blast from NCBI BLASTp, which you can download at the following link:
	https://www.biostars.org/p/6541/

Then you should be able to run the all-to-all blast by typing the following in the terminal
	$ ncbi-blast-2.2.24+/bin/blastp -db my_prot_blast_db -query good_proteins.fasta -outfmt 6 -out all-vs-all.tsv -num_threads 4
	(you can change the option -num_threads to the number of cores you have in your computer)

	now make sure you have an result file that is tab delimited, the format of this file should be:
		0    , 1      , 2  , 3       , 4       , 5      , 6  , 7   , 8  , 9   , 10    , 11
    	query, subject, %id, alignlen, mismatch, gapopen, qst, qend, sst, send, Evalue, bitscore

Now you can put the all-to-all data file(s) to the following folder: 
	InputFiles/BLASTp_AllToAll_Data (a.k.a "blastdir" in configuration.py)

Edit the configuration.py file with the parameters you are interested in testing. The parameters are:
	cutoffRatio:  
		This parameter is used to determine if two hits on the same protein overlapped enough to be consider the same area of the protein.
	evalueCutoff:
		This parameter is used to filter out the blast hits that has EValue larger then this number
The parameter file is a python file.  So make sure you follow python syntax when you are changing its contents!

Now open the folder in a terminal (FYI, I use Ubuntu) and type
	$ python run.py 

And the program should run!

The results should be located in Results/ (a.k.a. "borderResultdir" in configuration.py)

#################
# OUTPUT FORMAT #
#################

This program also dumps it's information through gpickle so you can load it up and do analysis using python.

The ouput format for the python gpickle dump is

	(moduleNumInfo,familyInfoWrap)
	, where
		moduleNumInfo=("Number of modules detected",NumberOfModulesDetected)
		familyInfoWrap=("ModuleFamilyInfo, Format: Dict\{proteinName, list[borders[moduleId,start,end]] \}", ModuleFamilyInfo)
		, where
			ModuleFamilyInfo= Dict{proteinName, list[borders] }"
			,where
				borders=[moduleId,start,end]

	i.e. if you want to access the dictionary information that contains the protein names as keys and the border information as the values you will have to get it through:

		loadedinfo[1][1]

		
This output should be located in GeneratedFiles/borderInformation (a.k.a "borderInfodir" in configuration.py)