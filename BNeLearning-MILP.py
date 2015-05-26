import os, sys, time
from subprocess import call
from multiprocessing import Pool
from multiprocessing import Process

from ScoreSet import ScoreSet

from create_folds import CreateFolds
from score_files import ScoreFile
from milp import ComputeMILP

def Search(scoreFile, treewidth):
 ComputeMILP(scoreFile, treewidth);
 call(["rm", "-f", os.path.splitext(scoreFile)[0] + ".data"], shell=False);

def _Search_Star_(args):
 return Search(args[0], args[1]);

def _Score_Star_((args)):
 return ScoreFile(args[0], args[1], args[2]);

def LearnDataset(datasetFile, folds, parentsLimit, ess):
 print "Managing dataset ", datasetFile
 start = time.time();

 N, trainingFiles = CreateFolds(datasetFile, folds, parentsLimit, ess);
 treewidths = [1000, 3, 4, 5];
 tw = 10;
 while N >= tw:
  treewidths.append(tw);
  tw = tw + 5;

 subprocesses = Pool(folds);
 scoreFiles = subprocesses.map(_Score_Star_, zip(trainingFiles, [parentsLimit] * folds, [ess] * folds));
 subprocesses.close();
 subprocesses.join();

 subprocesses = Pool(folds * len(treewidths) * 6);
 for scoreFile in scoreFiles:
  subprocesses.map(_Search_Star_, zip([scoreFile] * len(treewidths), treewidths));
 subprocesses.close();
 subprocesses.join();

 end = time.time();
 print "Finished managing dataset", datasetFile, "with time", end - start, ".";

def BNeLearning_MILP(fileList, folds, parentsLimit, ess):
 for datasetFile in fileList:
  LearnDataset(datasetFile, folds, parentsLimit, ess);

def Error():
 print "Usage:", sys.argv[0], "data_files", "number of folds", "ess", "parents_limit", "treewidth";
 exit(0);

if __name__ == "__main__":
 # try:
  BNeLearning_MILP(sys.argv[1:-3], int(sys.argv[-3]), float(sys.argv[-2]), int(sys.argv[-1]));
 # except:
 #  Error();
