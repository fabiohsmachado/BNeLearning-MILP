import sys
from milp import ComputeMILP

def SearchFold(scoreFile, treewidth):
 print "Managing dataset ", scoreFile;
 ComputeMILP(scoreFile, treewidth); 
 print "Finished managing dataset", scoreFile, "with time.\n";

def SearchFolds(fileList, treewidth):
 for scoreFile in fileList:
  SearchFold(scoreFile, treewidth);

def Error():
 print "Usage:", sys.argv[0], "score_files", "treewidth";
 exit(0);

if __name__ == "__main__":
 try:
  SearchFolds(sys.argv[1:-1], int(sys.argv[-1]));
 except:
  Error();
