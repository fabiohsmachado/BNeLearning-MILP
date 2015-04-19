#!/bin/python
#Read a list of datasets and score their variables using Gobnilp's scorer
import sys, os, time
from subprocess import call

def ScoreDatasetFile(pathToScorer, pathToDataset, ess, palim):
 print("Scoring the dataset", pathToDataset);
 start = time.clock();
 scoreFileName = os.path.splitext(pathToDataset)[0] + ".scores";
 scoreCommand = [pathToScorer, pathToDataset, str(ess), str(palim)];
 with open(scoreFileName, "w") as scoreFile:
  call(scoreCommand, stdout = scoreFile, shell = False);
 end = time.clock();
 print("Finished scoring with time", end - start, ".");
 return scoreFileName;

def Error():
 print("Usage:", sys.argv[0], "data_files", "ess", "parents_limit");
 exit(0);

def ScoreFiles(fileList, ess, parentsLimit):
 pathToScorer = "./lib/unix/scoring"; 
 return [ScoreDatasetFile(pathToScorer, datasetFile, ess, parentsLimit) for datasetFile in fileList if os.path.isfile(datasetFile)];
 
if __name__ == "__main__":
 try:
  print(ScoreFiles(sys.argv[1:], int(sys.argv[-2]), int(sys.argv[-1])));
 except:
  Error();
