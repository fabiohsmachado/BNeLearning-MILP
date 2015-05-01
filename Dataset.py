# Implements Dataset class 
import math
import os
from random import shuffle

from ScoreSet import ScoreSet

class Dataset:
 """ Class Dataset """
 def __init__(self, fileName = None, scoreFileName = None):
  self.name = "";
  self.pathToFiles = "";
  self.data = [];
  self.variablesCardinality = [];
  self.parentSets = [];
  self.parentScores = [];
  self.scoreSet = ScoreSet(scoreFileName);
  if(fileName is not None):
   self.ParseFile(fileName);

 @property 
 def variablesQuantity(self):
  return len(self.variablesCardinality);
  
 def ParseFile(self, fileName):
  self.name = os.path.splitext(os.path.basename(fileName))[0];
  with open(fileName, "r") as datasetFile:
   # self.variablesQuantity = int(datasetFile.readline());
   datasetFile.readline();
   self.variablesCardinality = [int(number) for number in datasetFile.readline().strip().split()];
   datasetFile.readline();
   self.data = [[int(number) for number in line.strip().split()] for line in datasetFile];
   self.data2 = [line for line in self.data if sum(line) != 0]

 def CloneWithoutData(self):
  cloneDataset = Dataset();
  cloneDataset.name = self.name;
  cloneDataset.variablesQuantity = self.variablesQuantity;
  cloneDataset.variablesCardinality = self.variablesCardinality;
  return cloneDataset;

 def KFoldGenerator(self, K, randomise = True):
  data = self.data;
  if randomise:
   data = list(data);
   shuffle(data);
 
  training = self.CloneWithoutData();
  validation = self.CloneWithoutData();
  dataPerFold = math.ceil(len(data) / K);

  for k in range(K):
   training.data = [line for i, line in enumerate(data) if math.floor(i/dataPerFold) != k]
   training.name = self.name + "." + str(k) + ".training";
   validation.data = [line for i, line in enumerate(data) if math.floor(i/dataPerFold) == k]
   validation.name = self.name + "." + str(k) + ".validation";
   yield training, validation;

 def WriteToFile(self, path = "./"):
  datasetFileName = path + "/" + self.name + ".data";
  with open(datasetFileName, "w") as datasetFile:
   datasetFile.write(str(self.variablesQuantity) + "\n");
   datasetFile.write(" ".join(map(str, self.variablesCardinality)) + "\n");
   datasetFile.write(str(len(self.data)) + "\n");
   datasetFile.write("\n".join(" ".join(map(str, dataLine)) for dataLine in self.data));
   datasetFile.write("\n");
  return datasetFileName;
