# Implements Dataset class 
import os

class ScoreSet:
 """ Class ScoreSet """
 def __init__(self, scoreFileName = None):
  self.parentSets = [];
  self.parentScores = [];
  self.variablesQuantity = 0;
  if(scoreFileName is not None):
   self.ParseScoreFile(scoreFileName);

 def ParseScoreFile(self, scoreFileName):
  with open(scoreFileName, "r") as datasetFile:
   self.variablesQuantity = int(datasetFile.readline());
   for _ in range(self.variablesQuantity):
    line = datasetFile.readline().strip().split();
    variable = int(line[0]);
    setSize = int(line[1]);
    self.parentScores.append([]);
    self.parentSets.append([]);
    for _ in range(setSize):
     line = datasetFile.readline().strip().split();
     self.parentScores[variable].append(float(line[0]));
     self.parentSets[variable].append([int (number) for number in line[2:]]);
