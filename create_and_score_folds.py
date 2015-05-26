import sys, time
from create_folds import CreateFolds
from score_files import ScoreFiles

def CreateAndScoreFolds(fileList, folds, parentsLimit, ess):
 for datasetFile in fileList:
  start = time.clock();
  print("Managing dataset ", datasetFile);
  validationFiles = CreateFolds(datasetFile, folds);
  scoreFiles = ScoreFiles(validationFiles, ess, parentsLimit);
  
  end = time.clock();
  print("Finished managing dataset", datasetFile, "with time", end - start, ".\n");

def Error():
 print("Usage:", sys.argv[0], "data_files", "number of folds", "ess", "parents_limit");
 exit(0);

if __name__ == "__main__":
 try:
  CreateAndScoreFolds(sys.argv[1:-3], int(sys.argv[-3]), int(sys.argv[-2]), int(sys.argv[-1]));
 except:
  Error();
