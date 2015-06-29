#!/bin/python
#Read a list of datasets and score their variables using Gobnilp's scorer
import sys, os
from subprocess import call

def ScoreDatasetFile(pathToScorer, pathToDataset, ess, palim):
 print "Scoring the dataset", pathToDataset ;

 scoreFileName = os.path.splitext(pathToDataset)[0] + ".scores";
 scoreCommand = [pathToScorer, pathToDataset, str(ess), str(palim)];
 with open(scoreFileName, "w") as scoreFile:
  call(scoreCommand, stdout = scoreFile, shell = False);

 print "Finished scoring file", scoreFileName, ".";
 return scoreFileName;

def ScoreFile(fileName, parentsLimit, ess):
 pathToScorer = "./lib/unix-cluster/scoring"; 
 if(os.path.isfile(fileName)):
  return ScoreDatasetFile(pathToScorer, fileName, ess, parentsLimit);
 else: return -1;

def ScoreFiles(fileList, parentsLimit, ess):
 return [ScoreFile(datasetFile, ess, parentsLimit) for datasetFile in fileList];

def Error():
 print("Usage:", sys.argv[0], "data_files", "parents_limit", "ess");
 exit(0);
 
if __name__ == "__main__":
 try:
  print(ScoreFiles(sys.argv[1:], int(sys.argv[-2]), float(sys.argv[-1])));
 except:
  Error();
