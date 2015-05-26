import os, sys, time
from subprocess import call

from create_folds import CreateFolds
from score_files import ScoreFiles
from milp import ComputeMILP

def CreateScoreAndSearchFolds(datasetFile, folds, parentsLimit, ess, treewidth):
 start = time.clock();
 print "Managing dataset ", datasetFile;
 validationFiles = CreateFolds(datasetFile, folds);
 scoreFiles = ScoreFiles(validationFiles, ess, parentsLimit);
 for scoreFile in scoreFiles:
  ComputeMILP(scoreFile, treewidth);
  call(["rm", "-f", os.path.splitext(scoreFile)[0] + ".data"], shell=False);
 end = time.clock();
 print "Finished managing dataset", datasetFile, "with time", end - start, ".\n";

def CreateScoreAndSearchFoldsFromList(fileList, folds, parentsLimit, ess, treewidth):
 for datasetFile in fileList:
  CreateScoreAndSearchFolds(datasetFile, folds, parentsLimit, ess, treewidth);

def Error():
 print "Usage:", sys.argv[0], "data_files", "number of folds", "ess", "parents_limit";
 exit(0);

if __name__ == "__main__":
 try:
  CreateScoreAndSearchFoldsFromList(sys.argv[1:-4], int(sys.argv[-4]), int(sys.argv[-3]), int(sys.argv[-2]), int(sys.argv[-1]));
 except:
  Error();
