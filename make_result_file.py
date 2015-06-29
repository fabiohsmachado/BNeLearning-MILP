import sys, os

def SaveResult(timeFileName, resultFile):
 nameList = os.path.basename(timeFileName).split('.');
 datasetName = nameList[-5];
 fold = nameList[-4];
 treewidth = nameList[-2][2:];

 with open(timeFileName, 'r') as timeFile:
  timeFile.readline();
  time = timeFile.readline()[:-1];
  timeFile.readline();
  timeFile.readline();
  timeFile.readline();
  score = timeFile.readline()[:-1];
  timeFile.readline();
  gap = timeFile.readline()[:-1];
  timeFile.readline();
  likelihood = timeFile.readline()[:-1];
  resultFile.write(datasetName + ',' + fold + ',' + treewidth + ',' + time + ',' + score + ',' + gap + ',' + likelihood + '\n');

def MakeResultFile(fileList):
 with open("BNeLearning.csv", 'w') as resultFile:
  resultFile.write("Dataset,Fold,Treewidth,Time,Score,Gap,Likelihood\n")
  for timeFileName in fileList:
   SaveResult(timeFileName, resultFile);

def Error():
 print "Usage:", sys.argv[0], "time_files";
 exit(0);

if __name__ == "__main__":
 try:
  MakeResultFile(sys.argv[1:]);
 except:
  Error();
