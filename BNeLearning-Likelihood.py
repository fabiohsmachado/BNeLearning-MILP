import sys
from measure_likelihood import MeasureLikelihood

def Likelihood(matrixFileName, ess):
 nameList = matrixFileName.split('.');
 datasetFileName = '.'.join(nameList[0:-3]) + ".validation.data";
 timeFileName = '.'.join(nameList[0:-1]) + ".time";

 likelihood = MeasureLikelihood(datasetFileName, matrixFileName, ess);

 with open(timeFileName, "a") as timeFile:
  timeFile.write("Likelihood of the Network:\n")
  timeFile.write(str(likelihood))
  timeFile.write('\n')

def BNeLearning_Likelihood(fileList, ess):
 for datasetFile in fileList:
  Likelihood(datasetFile, ess);

def Error():
 print "Usage:", sys.argv[0], "matrix_files", "ess";
 exit(0);

if __name__ == "__main__":
 try:
  BNeLearning_Likelihood(sys.argv[1:-1], float(sys.argv[-1]));
 except:
  Error();
