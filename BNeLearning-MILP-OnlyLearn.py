import os, sys, itertools
from subprocess import call
from multiprocessing import Pool
from multiprocessing import Process

from ScoreSet import ScoreSet

from create_folds import CreateFolds
from score_files import ScoreFile
from milp import ComputeMILP
from compact_folder import CompactFolder

def Search(scoreFile, treewidth):
 ComputeMILP(scoreFile, treewidth);
 call(["rm", "-f", os.path.splitext(scoreFile)[0] + ".data"], shell=False);

def _Search_Star_(args):
 return Search(args[0], args[1]);

def LearnDataset(scoreFiles, N):
 print "Start";

 if N >= 30:
  increment = 5;
 else:
  increment = 10;
 treewidths = [1000, 3, 4, 5];
 tw = 10;
 while N >= tw:
  treewidths.append(tw);
  tw = tw + increment;
 
 tasklist = list(itertools.product(scoreFiles, treewidths));
 subprocesses = Pool(4);
 subprocesses.map(_Search_Star_, tasklist, 4);
 subprocesses.close();
 subprocesses.join();

 print "Finish";

def Error():
 print "Usage:", sys.argv[0], "data_files", "number of folds", "parents_limit", "ess";
 exit(0);

if __name__ == "__main__":
 # try:
  LearnDataset(sys.argv[1:-1], int(sys.argv[-1]));
 # except:
 #  Error();
